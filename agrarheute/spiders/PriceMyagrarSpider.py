import scrapy
import urllib3
import urllib.request
import agrarheute.MyagrarspiderConfig as Config
from bs4 import BeautifulSoup


class PricemyagrarspiderSpider(scrapy.Spider):
    name = 'PriceMyagrarSpider'
    allowed_domains = ['https://www.myagrar.de']
    # start_urls = ['https://www.myagrar.de']

    headers={
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.myagrar.de',
        'pragma': 'no-cache',
        'referer': 'https://www.myagrar.de/',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    def start_requests(self):                
        for i in Config.relative_urls.values():
            yield scrapy.Request(Config.base_url.format(i))

    def parse(self, response):
        # url='https://myagrar.fact-finder.de/fact-finder/rest/v4/navigation/myagrar_magento_live_de?page=1&filter=CategoryPath%3APflanzenschutzmittel%2FKulturen%2FZuckerr%C3%BCben&sid=jJdLapiuOn31vQH3pqAmjs1gjsifJD&format=json'
        with urllib.request.urlopen(response.url) as url:
            data =  url.read()
            soup = BeautifulSoup(data)
            self.logger.info(soup)
      
