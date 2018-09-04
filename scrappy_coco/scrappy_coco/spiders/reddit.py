# -*- coding: utf-8 -*-
import scrapy

from scrappy_coco.items import RedditItem


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = []

    def __init__(self, subreddits='', **kwargs):
        self.start_urls = self.get_start_urls(subreddits)

    def parse(self, response):
        for thread in response.css('#siteTable .thing'):
            yield self.parse_thread(thread)

    def parse_thread(self, thread):
        item = RedditItem()
        item['upvotes'] = thread.css('.score.unvoted::attr(title)').extract_first()
        item['subreddit'] = thread.css('a.subreddit::attr(href)').extract_first()
        item['title'] = thread.css('a.title::text').extract_first()
        item['thread_url'] = thread.css('a.title::attr(href)').extract_first()
        item['comments_url'] = thread.css('a.comments::attr(href)').extract_first()
        return item

    def get_start_urls(self, subreddits):
        if subreddits:
            return ['http://old.reddit.com/r/{0}'.format(subreddit)
                    for subreddit
                    in subreddits.split(";")]
        else:
            return ['http://old.reddit.com/']