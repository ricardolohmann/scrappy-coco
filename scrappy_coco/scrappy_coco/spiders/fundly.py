from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrappy_coco.items import FundlyItem


class FundlySpider(CrawlSpider):
    """Web Scrapper for Fundly.

    This uses LinkExtractor to find next URLs.
    """
    name = 'fundly'
    allowed_domains = []
    start_urls = ['https://fundly.com/creative-projects']
    rules = [
        Rule(LinkExtractor(allow=r'creative-projects\?page=[0-9]+'),
             callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        for project in response.css('.f-b-light.one.f-ilb.f-m-r-xsmall.f-m-l-xsmall.f-m-b-medium'):
            yield self.parse_project_content(project)

    def parse_project_content(self, project_content):
        item = FundlyItem()
        item['url'] = 'https://fundly.com' + project_content.css('.f-db.f-fc-xdark::attr(href)').extract_first()
        item['title'] = project_content.css('.f-db.f-fc-xdark::text').extract_first()
        return item
