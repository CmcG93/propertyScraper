# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PropertyscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        #removing all the whitespace from returned data and removing \n's
        propertyFieldName = adapter.field_names()
        for fieldName in propertyFieldName:
            value = adapter.get(fieldName)
            adapter[fieldName] = value.strip().replace("\n", "")
        return item
