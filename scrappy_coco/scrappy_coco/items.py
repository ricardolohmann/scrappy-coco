# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KickstarterItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    # subtitle = scrapy.Field()
    category = scrapy.Field()
    owner = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    funded_money = scrapy.Field()
    funded_percentual = scrapy.Field()
    # fund_goal = scrapy.Field()


class FundlyItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    funded_money = scrapy.Field()
    currency = scrapy.Field()

class RedditItem(scrapy.Item):
    upvotes = scrapy.Field()
    subreddit = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    comments_url = scrapy.Field()
