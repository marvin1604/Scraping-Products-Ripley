import scrapy

#XPAth

#link    =  response.xpath('//a[starts-with(@class, "catalog")]/@href').getall()
#nombre   = response.xpath('//h1/text()').get()
#id    = response.xpath('//p[@class="sku-container"]//span[@class = "sku sku-value"]/text()').get()
#precio = response.xpath('//section[@class="product-info"]//dt[@class="product-price"]/text()').getall()

class SpiderRipley(scrapy.Spider):
    name       = 'ripley'
    start_urls = [
        'https://simple.ripley.com.pe/tecnologia/computacion/laptops?source=menu'
    ]
    custom_settings = {
        'FEED_URI'             : 'ripley.csv',
        'FEED_FORMAT'          : 'csv',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    }
    def parse(self, response):
        links_product = response.xpath('//a[starts-with(@class, "catalog")]/@href').extract()
        for link in links_product:
            #para que pueda trabajar en scraping hub necesitamos cambiar cb_kwargs por meta y get y getall por extract
            yield response.follow(link, callback = self.parse_link, meta={'url': response.urljoin(link)})

    def parse_link(self, response):
        link    = response.meta['url']
        name_product   = response.xpath('//h1/text()').get()
        id    = response.xpath('//p[@class="sku-container"]//span[@class = "sku sku-value"]/text()').get()
        price = response.xpath('//section[@class="product-info"]//dt[@class="product-price"]/text()').get()

        yield{
            'url'     : link,
            'name_product'   : name_product,
            'id'    : id,
            'price' : price
        }
