# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class ScrappyCocoPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['DATABASE_SERVER'],
            settings['DATABASE_PORT']
        )
        db = connection[settings['DATABASE_DB']]
        self.collection = db[settings['DATABASE_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        log.msg("Added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item
