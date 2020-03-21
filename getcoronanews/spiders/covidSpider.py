from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from urllib.parse import urlparse
import pandas as pd
from unidecode import unidecode

websites_data = pd.read_csv("data/websites.csv", index_col=0)

# List of districts
pt_df = pd.read_csv("data/pt.csv")
madeira_df = pd.read_csv("data/madeira.csv")
acores_df = pd.read_csv("data/acores.csv")


class CovidSpider(CrawlSpider):
    name = "covidnews"
    start_urls = websites_data.index.values.tolist()
    parsed_urls = [urlparse(url) for url in start_urls]
    allowed_domains = list(set(f"{url.netloc}" for url in parsed_urls))

    deny_links_rule = "|".join(["deporto", "economia", "cultura", "política"])
    rules = [Rule(LinkExtractor(allow=r"(corona|covid)", deny=deny_links_rule), follow=True, callback="parse_article")]

    def parse_article(self, response):
        """ Parses the article and returns the proper output"""

        parsed_url = urlparse(response.url)
        origin_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        title_path = websites_data.loc[origin_url, "path_to_title"]
        content_path = websites_data.loc[origin_url, "path_to_content"]

        title = response.css(title_path + "::text").get()
        content = unidecode(".".join([x.get() for x in response.css(content_path + " p ::text")]))
        content = re.sub(r"\r|\n", " ", content)

        # Try and find the date
        datetime = re.findall(r"(\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2})", response.url)
        if len(datetime) > 0:
            datetime = datetime[0]
        else:
            datetime = re.findall(r"(\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2})", response.text)
            if len(datetime) == 0:
                datetime = None
            else:
                datetime = datetime[0]

        if title is not None:
            return {
                "news_date": datetime,
                "url": response.url,
                "title": title,
                "content": content,
            }
