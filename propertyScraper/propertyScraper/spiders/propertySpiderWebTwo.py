import scrapy
from propertyScraper.items import PropertyItemWebOneSale

class PropertyspiderWebTwoSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        '../data/propertyDataWebsiteTwo.xlsx' : {
            'format': 'xlsx',
            'overwrite' : True
            }
        }
    }
    name = "propertySpiderWebTwo"
    allowed_domains = ["www.rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/overseas-property-for-sale/Ireland.html"]
    
    def parse(self, response):
        properties = response.css('.propertyCard-details')
        propertyItem = PropertyItemWebOneSale()
        for property in properties:
            relative_url = property.css("a").attrib["href"]
            listingUrl = "https://www.rightmove.co.uk" + relative_url
            propertyItem["address"] = property.css("span ::text").get()
            propertyItem["amenities"] = property.css("h2 ::text").get().strip()
            propertyItem["url"] = listingUrl
            yield propertyItem 
            yield scrapy.Request(listingUrl, callback=self.parseWebsiteTwoPrice)
        
        pageIndex = 1008
        if len(properties) == 25:
            for pageNumber in range(24,pageIndex,24):
                if pageNumber < pageIndex:
                    next_page_url = 'https://www.rightmove.co.uk/overseas-property-for-sale/Ireland.html?index={nextPage}'.format(nextPage=pageNumber)
                    print(next_page_url)
                    yield response.follow(next_page_url, callback=self.parse)

            
    def parseWebsiteTwoPrice(self, response):
        propertyItem = PropertyItemWebOneSale()
        propertyItem["price"]=response.xpath("//article/div/div/div/span//text()").get()
        yield propertyItem 