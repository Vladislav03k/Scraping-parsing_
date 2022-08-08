import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from castoramaparser.items import CastoramaparserItem

class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    start_urls = ['http://castorama.ru/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/tile/wall-tile']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaparserItem(), response=response)
        loader.add_xpath('name', "//h1[@class='product-essential__name hide-max-small']/text()")
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('photos', "//ul/li/img/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1[@class='product-essential__name hide-max-small']/text()").get()
        # price = response.xpath("//span[@class='price']/span/span/text()").get()
        # url = response.url
        # photos = response.xpath("//ul/li/img/@src").getall()
        # yield CastoramaparserItem(name=name, price=price, url=url, photos=photos)
