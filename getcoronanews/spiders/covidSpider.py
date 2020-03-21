from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from datetime import datetime as dt
from urllib.parse import urlparse
import pandas as pd
from unidecode import unidecode

websites_data = pd.read_csv("websites.csv", sep=";", index_col=0)


class CovidSpider(CrawlSpider):
    name = "covidnews"
    start_urls = websites_data.index.values
    parsed_urls = [urlparse(url) for url in start_urls]
    allowed_domains = list(set(f"{url.netloc}" for url in parsed_urls))

    deny_links_rule = "|".join(["deporto", "economia", "cultura", "política"])
    rules = [Rule(LinkExtractor(allow=r"(corona|covid)", deny=deny_links_rule), follow=True, callback="parse_article")]

    @staticmethod
    def parse_article(self, response):
        """ Parses the article and returns the proper output"""

        parsed_url = urlparse(response.url)
        origin_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        title_path = websites_data.loc[origin_url, "path_to_title"]
        date_path = websites_data.loc[origin_url, "path_to_date"]
        content_path = websites_data.loc[origin_url, "path_to_content"]

        title = response.css(title_path).get()
        content = unidecode(".".join([x.get() for x in response.css(content_path + " p ::text")]))
        content = re.sub(r"\r|\n", " ", content)
        try:
            datetime = response.css(date_path).attrib['datetime']
            datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d")
        except:
            datetime = None
        if title is not None:
            return {
                "news_date": datetime,
                "url": response.url,
                "title": title,
                "content": content,
            }
