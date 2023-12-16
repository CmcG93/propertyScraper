import scrapy
from propertyScraper.items import PropertyItemWebOneRent


class PropertyspiderSpider(scrapy.Spider):
    name = "propertySpider"
    allowed_domains = ["www.property.ie", "www.daft.ie"]
    # can add multipe URL's here for spider to crawl through
    start_urls = ["https://www.property.ie/property-to-let/property-to-let/ireland/"]

    def parse(self, response):
        properties = response.css('div.search_result')
        propertyItem = PropertyItemWebOneRent()
        
        for property in properties:
            propertyItem["address"] = property.css("h2 a::text").get()
            propertyItem["price"] = property.css("h3 ::text").get()
            propertyItem["amenities"] = property.css("h4 ::text").get()
            propertyItem["url"] = property.css("h2 a").attrib['href']
            yield propertyItem

        totalPagesHtml = response.css('#pages > a:nth-child(9) ::text').get()
        totalPages = int(totalPagesHtml)

        next_page = response.css('#pages > a:nth-child(10) ::attr(href)').get()

        for pageNumber in range(totalPages):
            ++pageNumber
            if next_page is not None:
                next_page_url = "https://www.property.ie/property-to-let/ireland/price_international_rental-onceoff_standard/p_" + str(pageNumber)
            else:
                break
            yield response.follow(next_page_url, callback=self.parse)
            
             
