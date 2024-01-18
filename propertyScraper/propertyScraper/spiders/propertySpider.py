import scrapy
from propertyScraper.items import PropertyItemWebForSale

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
        propertyItem = PropertyItemWebForSale()
        
        for property in properties:
            propertyItem["address"] = property.css("h2 a::text").get()
            propertyItem["price"] = property.css("h3 ::text").get()
            propertyItem["amenities"] = property.css("h4 ::text").get()
            propertyItem["url"] = property.css("h2 a").attrib['href']
            yield propertyItem

        next_page_url = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.logger.debug("No more pages to follow")

class PropertyspiderWebTwoSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        'data/propertyData_WebTwo.xlsx' : {
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
        #~~~~~~~~~~IS THIS NEEDED~~~~~~~~~~~~~~
        propertyItem = PropertyItemWebForSale()
        for property in properties:
            relative_url = property.css("a").attrib["href"]
            listingUrl = "https://www.rightmove.co.uk" + relative_url
            #propertyItem = PropertyItemWebForSale()
            propertyItem["address"] = property.css("span ::text").get()
            propertyItem["amenities"] = property.css("h2 ::text").get().strip()
            propertyItem["url"] = listingUrl
            yield scrapy.Request(listingUrl, callback=self.parseWebsiteTwoPrice, meta={'propertyItem': propertyItem})
        
        pageIndex = 1008
        #is this needed as properties is already 25
        if len(properties) == 25:
            for pageNumber in range(24,pageIndex,24):
                if pageNumber < pageIndex:
                    next_page_url = 'https://www.rightmove.co.uk/overseas-property-for-sale/Ireland.html?index={nextPage}'.format(nextPage=pageNumber)
                    yield response.follow(next_page_url, callback=self.parse)

    def parseWebsiteTwoPrice(self, response):
        propertyItem = response.meta.get('propertyItem', PropertyItemWebForSale())
        propertyItem["price"]=response.xpath("//article/div/div/div/span//text()").get()
        yield propertyItem 

class PropertyspiderWebThreeSpider(scrapy.Spider):
    custom_settings = {
    'FEEDS' : {
        'data/propertyData_WebThree.xlsx' : {
            'format': 'xlsx',
            'overwrite' : True
            }
        },
    "AUTOTHROTTLE_ENABLED" : False
    }
    name = "propertySpiderWebThree"
    allowed_domains = ["www.daft.ie"]
    start_urls = ["https://www.daft.ie/property-for-sale/ireland"]

    def parse(self, response):
        self.logger.debug(f"Scraping page: {response.url}")
        #getting all url's that have "/for-sale/" as they are the only required.
        properties = response.xpath('//a[contains(@href, "/for-sale/")]/@href').getall()        
        for property in properties:
            listingUrl = "https://www.daft.ie" + property
            propertyItem = PropertyItemWebForSale()
            propertyItem["url"] = listingUrl
            yield scrapy.Request(listingUrl, callback=self.parseWebsiteThreeInfo, meta={'propertyItem': propertyItem})
        
        next_page_url = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.logger.debug("No more pages to follow")
                      
    def parseWebsiteThreeInfo(self, response):
        propertyItem = response.meta.get('propertyItem', PropertyItemWebForSale())
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
                    # Both selectors failed or didn't contain the Euro symbol, set price to appropriate response.
                    propertyItem["price"] = "Price not correctly listed view url for more info."

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