# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class PropertyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class PropertyItemWebForSale(scrapy.Item):
    county = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    amenities = scrapy.Field()
    url = scrapy.Field()

class PropertyItemWebForRent(scrapy.Item):
    county = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    amenities = scrapy.Field()
    url = scrapy.Field()
