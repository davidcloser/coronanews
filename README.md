# Portuguese newspapaer coronavirus news crawler
This crawler will crawl portuguese newspapers in search for Coronavirus news.
Based on Scrapy

# Installation
Install requirements.txt

# Usage
Run the crawler by using on the getcoronanews folder
```bash
scrapy crawl covidnews -o covidnews.csv
```

# Feed more news sources
To feed more news sources, update the websites.csv file by adding url the a new newspaper source, the css selector to the title and to the content of the articles. 
