# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter


#class BbcPipeline:
    #def process_item(self, item, spider):
        #return item


import logging
import pymongo
import sqlite3

class MongodbPipeline(object):
    collection_name = input('Enter the name of the collection in which you would like to save your data : ')

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://mohammed:testtest@cluster0.qz6hc.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.client["BBC_ARTICLES"]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item