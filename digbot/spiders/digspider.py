# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.markup import remove_tags, remove_tags_with_content
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import scrapy
import tldextract
import redis
from digbot.items import PageItem


class DigSpider(RedisSpider):
    name = 'digspider'
    link_extractor = SgmlLinkExtractor()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def is_domestic(self, url):
        return tldextract.extract(url).tld == 'uz'

    def is_domain_in_white_list(self, url):
        r = redis.Redis(connection_pool=self.pool)
        domain = tldextract.extract(url).registered_domain
        return r.sismember('domain_whitelist', domain)

    def parse(self, response):
        hxs = scrapy.Selector(response)
        refer_links = self.link_extractor.extract_links(response)
        tld_links = [link.url for link in refer_links if self.is_domestic(link.url)]

        item = PageItem()
        try:
            item['title'] = hxs.xpath('/html/head/title/text()').extract()[0]
        except:
            item['title'] = tldextract.extract(response.url).registered_domain
        yield item

        r = redis.Redis(connection_pool=self.pool)

        for link in tld_links:
            if not r.sismember('visited_urls', link):
                if self.is_domain_in_white_list(link):
                    scrapy.log.msg('Following link {}'.format(link))
                    r.sadd('visited_urls', link)
                    yield scrapy.http.Request(url=link, callback=self.parse)
                else:
                    scrapy.log.msg('Domain not in white list {}'.format(link))
