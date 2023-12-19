import scrapy
import pandas as pd
from propertyScraper.items import PropertyItemWebOneSale

class PropertyspiderSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        'data/propertyData_WebOne.xlsx' : {
            'format': 'xlsx',
            'overwrite' : True
            }
        }
    }
    name = "propertySpider"
    allowed_domains = ["www.property.ie"]
    start_urls = ["https://www.property.ie/property-for-sale/ireland/price_international_rental-onceoff_standard/" ]
    
    def parse(self, response):
        properties = response.css('div.search_result')
        propertyItem = PropertyItemWebOneSale()
        
        for property in properties:
            propertyItem["address"] = property.css("h2 a::text").get().strip()
            propertyItem["price"] = property.css("h3 ::text").get()
            propertyItem["amenities"] = property.css("h4 ::text").get()
            propertyItem["url"] = property.css("h2 a").attrib['href']
            yield propertyItem

        # totalPagesHtml = response.css('#pages > a:nth-child(9) ::text').get()
        # totalPages = int(totalPagesHtml)

        # next_page = response.css('#pages > a:nth-child(10) ::attr(href)').get()

        # for pageNumber in range(totalPages):
        #     ++pageNumber
        #     if next_page is not None:
        #         next_page_url = "https://www.property.ie/property-for-sale/ireland/price_international_rental-onceoff_standard/p_" + str(pageNumber)
        #     else:
        #         break
        #     yield response.follow(next_page_url, callback=self.parse)

class PropertyspiderWebTwoSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        'data/propertyData_WebTwo.xlsx' : {
            'format': 'xlsx',
            'overwrite' : False
            }
        }
    }
    name = "propertySpider"
    allowed_domains = ["www.rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/overseas-property-for-sale/Ireland.html"]
    
    def parse(self, response):
        properties = response.css('.propertyCard-details')
        propertyItem = PropertyItemWebOneSale()
        for property in properties:
            relative_url = property.css("a").attrib["href"]
            listingUrl = "https://www.rightmove.co.uk" + relative_url
            propertyItem = PropertyItemWebOneSale()
            propertyItem["address"] = property.css("span ::text").get()
            propertyItem["amenities"] = property.css("h2 ::text").get().strip()
            propertyItem["url"] = listingUrl
            yield scrapy.Request(listingUrl, callback=self.parseWebsiteTwoPrice, meta={'propertyItem': propertyItem})
        
        # pageIndex = 1008
        # if len(properties) == 25:
        #     for pageNumber in range(24,pageIndex,24):
        #         if pageNumber < pageIndex:
        #             next_page_url = 'https://www.rightmove.co.uk/overseas-property-for-sale/Ireland.html?index={nextPage}'.format(nextPage=pageNumber)
        #             print(next_page_url)
        #             yield response.follow(next_page_url, callback=self.parse)

    def parseWebsiteTwoPrice(self, response):
        propertyItem = response.meta.get('propertyItem', PropertyItemWebOneSale())
        propertyItem["price"]=response.xpath("//article/div/div/div/span//text()").get()
        yield propertyItem 
    