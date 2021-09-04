# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter, JsonItemExporter
import os


class CsvExportPipeline():
    fp = lambda self, x: f"C:/Users/user/Desktop/Practice/Python/Scrapy/AirbnbListings/csv/{x}.csv"
    fields_to_export = ['Title', 'Rating', 'Guests', 'Features', 'Price', 'Link']

    def open_spider(self, spider):
        for fp in [self.fp(dest) for dest in spider.destinations]:
            if os.path.isfile(fp): os.remove(fp)

        self.exporters = {}

    def __exporter_for_item(self, item):
        destination = item['Destination']
        if destination not in self.exporters.keys():
            file = open(self.fp(destination), 'wb')
            exp = CsvItemExporter(file, fields_to_export=self.fields_to_export)
            self.exporters[destination] = exp

        return self.exporters[destination]


    def process_item(self, item, spider):
        self.__exporter_for_item(item).export_item(item)
        return item

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()


class JsonExportPipeline():
    fp = lambda self, x: f"C:/Users/user/Desktop/Practice/Python/Scrapy/AirbnbListings/json/{x}.json"
    fields_to_export = ['Title', 'Rating', 'Guests', 'Features', 'Price', 'Link']

    def open_spider(self, spider):
        for fp in [self.fp(dest) for dest in spider.destinations]:
            if os.path.isfile(fp): os.remove(fp)

        self.exporters = {}

    def __exporter_for_item(self, item):
        destination = item['Destination']
        if destination not in self.exporters.keys():
            file = open(self.fp(destination), 'wb')
            exp = JsonItemExporter(file, fields_to_export=self.fields_to_export, indent=2)
            self.exporters[destination] = exp

        return self.exporters[destination]


    def process_item(self, item, spider):
        self.__exporter_for_item(item).export_item(item)
        return item

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
