# -*- coding: utf-8 -*-
import scrapy

from scrappy_coco.items import RedditItem


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = []
    start_urls = ['http://old.reddit.com/']

    def parse(self, response):
        for thread in response.css('#siteTable .thing'):
            yield self.parse_thread(thread)

    def parse_thread(self, thread):
        item = RedditItem()
        item['upvotes'] = thread.css('.score.upvote::text').extract()
        item['subreddit'] = thread.css('a.subreddit::attr(href)').extract()
        item['title'] = thread.css('a.title::text').extract()
        item['thread_url'] = thread.css('a.title::attr(href)').extract()
        item['comments_url'] = thread.css('a.comments::attr(href)').extract()
        return item
