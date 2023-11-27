# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PropertyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class PropertyItem(scrapy.Item):
    address = scrapy.Field()
    price = scrapy.Field()
    ammenities = scrapy.Field()
    url = scrapy.Field()
