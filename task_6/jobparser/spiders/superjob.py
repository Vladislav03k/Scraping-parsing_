import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem

class SJSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=phython&geo%5Br%5D%5B0%5D=3',
                  'https://mo.superjob.ru/vacancy/search/?keywords=phython']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div/div/div/div/div/div/div/div/div/div/span/a[@target='_blank']").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)
        pass

    def parse_vacancy(self, response: HtmlResponse):
        name = response.xpath('//h1').gettext()
        #list_salary = response.xpath('//div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/span').getall()
        #salary =    #не хватает времени на поиск решения данной проблемы, я реализовал паука без зарплаты
        url = response.url
        return JobparserItem(name=name, url=url)

