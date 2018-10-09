# -*- coding: utf-8 -*-
import logging
import logging.config
import os.path
import scrapy
import yaml

from scrappy_coco.items import RedditItem


REDDIT_URL = 'http://old.reddit.com'
SUBREDDIT_URL = 'http://old.reddit.com/r/{0}'

# Init logging
logging_file = os.path.dirname(__file__) + '/../logging.yaml'
with open(logging_file, 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = []

    def __init__(self, subreddits='', **kwargs):
        subreddits = subreddits.split(';')
        self.start_urls = self.get_start_urls(subreddits)
        logging.info('Started URLs: %s', self.start_urls)

    def parse(self, response):
        logger.info('Parsing response %s', response.url)
        threads = response.css('#siteTable .thing')
        logger.info('Found %s threads', len(threads))
        for thread in threads:
            yield self.parse_thread(thread)

    def parse_thread(self, thread):
        logger.info('Parsing thread')
        item = RedditItem()
        item['upvotes'] = thread.css('.score.unvoted::attr(title)').extract_first()
        item['subreddit'] = thread.css('a.subreddit::attr(href)').extract_first()
        item['title'] = thread.css('a.title::text').extract_first()
        item['url'] = REDDIT_URL + thread.css('a.title::attr(href)').extract_first()
        item['comments_url'] = thread.css('a.comments::attr(href)').extract_first()
        logger.info('Parsed: %s', item['url'])
        return item

    def get_start_urls(self, subreddits):
        if subreddits:
            return [SUBREDDIT_URL.format(subreddit)
                    for subreddit
                    in subreddits]
        else:
            return [REDDIT_URL]
