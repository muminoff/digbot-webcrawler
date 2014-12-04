# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.markup import remove_tags, remove_tags_with_content
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import scrapy
import tldextract
import html2text
import redis
from digbot.items import PageItem


class DigSpider(RedisSpider):
    name = 'digspider'
    link_extractor = SgmlLinkExtractor()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def is_domestic(self, url):
        return tldextract.extract(url).tld == 'uz'

    def parse(self, response):
        hxs = scrapy.Selector(response)
        refer_links = self.link_extractor.extract_links(response)
        tld_links = [link.url for link in refer_links if self.is_domestic(link.url)]

        item = PageItem()
        item['title'] = hxs.xpath('/html/head/title/text()').extract()[0]
        # item['content'] = html2text.html2text(response.body.decode('utf8'))
        yield item

        filtered_links = []
        r = redis.Redis(connection_pool=self.pool)

        for link in tld_links:
            if not r.sismember('visited_urls', link):
                r.sadd('visited_urls', link)
                filtered_links.append(link)
                yield scrapy.http.Request(url=link, callback=self.parse)
