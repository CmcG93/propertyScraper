import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class PropertyspiderSpider(scrapy.Spider):
    name = "propertySpider"
    allowed_domains = ["www.property.ie"]
    # can add multipe URL's here for spider to crawl through
    start_urls = ['https://www.property.ie/property-for-sale/ireland/price_international_rental-onceoff_standard/' +str(x) for x in range(1,617)]

    rules = (
        Rule(LinkExtractor(allow=r"/[0-9]+_"), callback='parse', follow=False),
    )

    def parse(self, response):
        properties = response.css('div.search_result')
        for property in properties:
            yield{
                "address"    : property.css("h2 a::text").get().replace("\n", ""),
                "price"      : property.css("h3 ::text").get().replace("\n", ""),
                "ammenities" : property.css("h4 ::text").get().replace("\n", ""),
                "url"        : property.css("h2 a").attrib['href']
            }

        # next_page = response.css('#pages > a:nth-child(10) ::attr(href)').get().split("/")[-2]

        # if next_page is not None:
        #     next_page_url = "https://www.property.ie/property-for-sale/ireland/price_international_rental-onceoff_standard/p_"
        #     print("\n\n\n\n" + next_page + "\n\n\n\n")
        # yield response.follow(next_page_url, callback=self.parse, dont_filter=True)
            
