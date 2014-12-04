# -*- coding: utf-8 -*-
import scrapy


class CrawlSpider(scrapy.Spider):
    name = "crawl"
    allowed_domains = ["digbot"]
    start_urls = (
        'http://www.digbot/',
    )

    def parse(self, response):
        pass
