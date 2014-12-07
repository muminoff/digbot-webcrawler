# -*- coding: utf-8 -*-

import scrapy


class PageItem(scrapy.Item):
    title = scrapy.Field()
    charset = scrapy.Field()
    content = scrapy.Field()
    last_crawled = scrapy.Field()
    spider = scrapy.Field()
