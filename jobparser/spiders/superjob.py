import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=3&page=1',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=4&geo%5Br%5D%5B1%5D=2&geo%5Br%5D%5B2%5D=5&page=1']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//body //a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//body //span [@class="-gENC _1TcZY Bbtm8"]/ a/@href').getall()

        for link in links:
            l = 'https://www.obninsk.superjob.ru' + link
            yield response.follow(l, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        print('***** superjob', name)
        salary = response.xpath('//span[@class="_4Gt5t _2nJZK"]//text()').getall()
        place = response.xpath('//span[@class="_35ziJ _1TcZY dAWx1"]//text()').get()
        url = response.url
        yield JobparserItem(name=name, salary=salary, place=place, url=url)