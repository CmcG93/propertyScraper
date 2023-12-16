# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PropertyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class PropertyItemWebOneSale(scrapy.Item):
    address = scrapy.Field()
    price = scrapy.Field()
    amenities = scrapy.Field()
    url = scrapy.Field()

class PropertyItemWebOneRent(scrapy.Item):
    address = scrapy.Field()
    price = scrapy.Field()
    amenities = scrapy.Field()
    url = scrapy.Field()
