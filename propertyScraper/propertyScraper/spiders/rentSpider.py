import scrapy
from propertyScraper.items import PropertyItemWebForRent

class RentspiderSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        'data/rentData_WebOne.xlsx' : {
            'format': 'xlsx',
            'overwrite' : True
            }
        }
    }
    name = "rentSpider"
    allowed_domains = ["www.property.ie"]
    start_urls = ["https://www.property.ie/property-to-let/property-to-let/ireland/"]

    def parse(self, response):
        properties = response.css('div.search_result')
        propertyItem = PropertyItemWebForRent()
        
        for property in properties:
            propertyItem["address"] = property.css("h2 a::text").get()
            propertyItem["price"] = property.css("h3 ::text").get()
            propertyItem["amenities"] = property.css("h4 ::text").get()
            propertyItem["url"] = property.css("h2 a").attrib['href']
            yield propertyItem

        # totalPagesHtml = response.css('#pages > a:nth-child(9) ::text').get()
        # totalPages = int(totalPagesHtml)

        # next_page = response.css('#pages > a:nth-child(10) ::attr(href)').get()

        next_page_url = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.logger.debug("No more pages to follow")
            
class RentspiderWebTwoSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        'data/rentData_WebTwo.xlsx' : {
            'format': 'xlsx',
            'overwrite' : True
            }
        }
    }
    name = "rentSpiderWebTwo"
    allowed_domains = ["www.daft.ie"]
    start_urls = ["https://www.daft.ie/property-for-rent/ireland"]

    def parse(self, response):
        self.logger.debug(f"Scraping page: {response.url}")
        #getting all url's that have "/for-rent/" as they are the only required.
        properties = response.xpath('//a[contains(@href, "/for-rent/")]/@href').getall()        
        for property in properties:
            listingUrl = "https://www.daft.ie" + property
            propertyItem = PropertyItemWebForRent()
            propertyItem["url"] = listingUrl
            yield scrapy.Request(listingUrl, callback=self.parseWebsiteTwoInfo, meta={'propertyItem': propertyItem})
        
        next_page_url = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.logger.debug("No more pages to follow")
                      
    def parseWebsiteTwoInfo(self, response):
        propertyItem = response.meta.get('propertyItem', PropertyItemWebForRent())
        try:
            priceSelector = response.css('main div:nth-child(3) div div div:nth-child(2) div:nth-child(3) p:nth-child(2) ::text')
            if priceSelector and '€' in priceSelector.get():
                propertyItem["price"] = priceSelector.get()
            else:
                # Check if the second CSS selector yields a result with a Euro symbol
                fallbackPriceSelector = response.css("h2 ::text")
                if fallbackPriceSelector and '€' in fallbackPriceSelector.get():
                    propertyItem["price"] = fallbackPriceSelector.get()
                else:
                    # Both selectors failed or didn't contain the Euro symbol, set price to None or handle as needed
                    propertyItem["price"] = None

            # Extract other data
            amenities = response.xpath("//main/div[3]/div[1]/div[1]/div/div[2]/div[2]//text()").getall()
            fullAmenityList = ", ".join(amenities)
            propertyItem["address"] = response.css("h1 ::text").get()
            propertyItem["amenities"] = fullAmenityList

            # Check if the address is None, and if so, skip the entire item
            if propertyItem["address"] is None:
                self.logger.debug("Skipping item due to missing address.")
                return

            yield propertyItem

        except TypeError:
            pass