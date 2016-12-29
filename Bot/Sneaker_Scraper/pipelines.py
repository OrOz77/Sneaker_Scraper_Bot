# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from Sneaker_Scraper.MongoDB.config import MONGODB_URI, MONGODB_DB


class NikePipeline(object):
    def process_item(self, item, spider):
        return item

#Pipeline for storing to MongoDB
class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=MONGODB_URI,
            mongo_db=MONGODB_DB
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[item['urlSource']]   #url source is collection name (ie Nike.com, Adidas.com, etc)
        collection.update_one(
            {
                'modelNumber': item['modelNumber']      #index collection by modelNumber
            },
            {
                '$set': dict(item)                      #update item. TODO look into only updating size field, but allows upsert to add entire item
            },
                upsert=True)                            #upsert allows new entry if update not found

        return item
