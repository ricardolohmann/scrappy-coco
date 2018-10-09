# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

import pymongo

from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class MongoDBPipeline(object):

    def __init__(self, server, port, user, password):
        logger.info('Init MongoDB Pipeline')
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.database = settings['DATABASE_DB']
        self.collection = settings['DATABASE_COLLECTION']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings['DATABASE_SERVER'],
            settings['DATABASE_PORT'],
            settings['DATABASE_USER'],
            settings['DATABASE_PASSWORD'],
        )

    def open_spider(self, spider):
        logger.info('Open spider MongoDB')
        self.client = pymongo.MongoClient(host=self.server,
                                          port=self.port,
                                          username=self.user,
                                          password=self.password,
                                          authSource='admin')
        self.db = self.client[self.database]

    def close_spider(self, spider):
        logger.info('Close spider MongoDB')
        self.client.close()

    def process_item(self, item, spider):
        logger.info('Store in MongoDB: %s', item['url'])
        for data in item:
            if not data:
                logger.warning('Drop due missing data')
                raise DropItem('Missing {0}!'.format(data))
        self.db[self.collection].replace_one({'url': item['url']},
                                             dict(item),
                                             upsert=True)
        return item
