import scrapy
from scrapy.http import HtmlResponse
from castorama_scraper.items import CastoramaScraperItem
#from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class CastoscraperSpider(scrapy.Spider):
    name = 'castoscraper'
    allowed_domains = ['castorama.ru']
    #start_urls = ['https://www.castorama.ru/gardening-and-outdoor/gardening-equipment/trimmers-and-braids']


    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('query')}"]


    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="product-card__img-link"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaScraperItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span [@class="price"]//text()')
        loader.add_xpath('photos', '//div[@class ="js-zoom-container"]//img/@data-src')
        loader.add_value('url', response.url)
        yield loader.load_item()


    #def parse_ads(self, response: HtmlResponse):

        #name = response.xpath('//h1/text()').getall()
        #price = response.xpath('//span [@class="price"]//text()').getall()
        #photos = response.xpath('//div[@class ="js-zoom-container"]//img/@data-src').getall()
        #url = response.url
        #yield CastoramaScraperItem(name=name, price=price, photos=photos,url=url)

