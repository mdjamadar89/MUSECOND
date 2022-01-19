from asyncio.log import logger
from curses import meta
from gc import callbacks
import logging
from urllib import request
import scrapy
import agrarheute.config as config
from agrarheute.config import logger




class agrarheuteSpider(scrapy.Spider):
    name = 'agrarheuteSpider'
    allowed_domains = ['markt.agrarheute.com']
    #start_urls = ['https://markt.agrarheute.com']
    #base_url = 'https://markt.agrarheute.com{}'
    #relative_urls=['/marktfruechte/','/tiere/','/futtermittel/','/duengemittel/','/diesel-5','/kuhmilch-25']

    
    # logging.basicConfig(level=logging.ERROR,format='%(asctime)s  [%(name)s] %(levelname)s  %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename='productExtract.log')
    # logger = logging.getLogger()

    def start_requests(self):
        for i in config.relative_urls:
            yield scrapy.Request(config.base_url.format(i))

    def parse(self, response):
        logger.setLevel(logging.ERROR)
        logger.info('Parse function called on %s', response.url)
        try:

            for i,j in zip(response.xpath("//div[@class='cat-card col-12 col-sm-6 card text-center']/a"),response.xpath("//div[@class='cat-card col-12 col-sm-6 card text-center']/h2")):
                logger.info('xpath called on {} and {}'.format(i,j))
                link = i.xpath(".//@href").get()
                name = j.xpath(".//text()").get()
           
                absolute_link = response.urljoin(link)

           
                yield response.follow(url=absolute_link,callback = self.extract_Product_Data,meta={'sub_type':name} )
                logger.info('yield  called to follow  %s',absolute_link)

        except Exception as e:
            logger.critical('Exception {} occured '.format(e))

    
    def extract_Product_Data(self,response):
        logger.info('Parse function called on %s', response.url)
        try:

            for i in response.xpath("//table/tbody/tr"):
                logger.info('xpath called on {}'.format(i))
          
                subtype_name =response.request.meta['sub_type']
                product = i.xpath(".//td[1]/text()").get()
                kw = i.xpath(".//td[2]/text()").get()
                price,unit = kw.split("/")
                vorwoche = i.xpath(".//td[3]/text()").get()
                spanne = i.xpath(".//td[4]/text()").get()

                yield{
                
                    'Category':subtype_name,
                    'Product':{'product_name':product,'price':price,'unit':unit,'vorwoche':vorwoche,'spanne':spanne}
                
                }
                logger.info('final yield  called on product  %s',product)

        except Exception as e:
            logger.critical('Exception {} occured '.format(e))


             

            
