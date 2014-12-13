# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.markup import remove_tags, remove_tags_with_content
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from digbot.items import PageItem
from digbot import settings
import scrapy
import tldextract
import redis


class DigbotSpider(RedisSpider):
    name = 'digspider'
    link_extractor = SgmlLinkExtractor()
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

    def is_domestic(self, url):
        return tldextract.extract(url).tld == 'uz'

    def is_domain_in_white_list(self, url):
        r = redis.Redis(connection_pool=self.pool)
        domain = tldextract.extract(url).registered_domain
        return r.sismember(self.name + ':domain_whitelist', domain)

    def get_domain(self, url):
        return tldextract.extract(url).registered_domain

    def parse(self, response):
        hxs = scrapy.Selector(response)
        refer_links = self.link_extractor.extract_links(response)
        tld_links = [
            link.url for link in refer_links if self.is_domestic(link.url)
        ]

        item = PageItem()
        item['url'] = response.url

        try:
            item['title'] = hxs.xpath('/html/head/title/text()').extract()[0].strip()
        except:
            item['title'] = tldextract.extract(response.url).registered_domain
        
        try:
            item['content'] = response.body
        except:
            item['content'] = response.body_as_unicode()

        # FIXME if failure consider following options in try mode
        # response._body_inferred_encoding()
        # response._body_declared_encoding()
        # response._headers_encoding()
        item['charset'] = response.encoding

        yield item

        r = redis.Redis(connection_pool=self.pool)
        new_domains = self.name + ':new_domains'

        for link in tld_links:
            visited_urls = '{}:{}:visited_urls'.format(self.name, self.get_domain(link))
            if not r.sismember(visited_urls, link):
                if self.is_domain_in_white_list(link):
                    scrapy.log.msg('Following link {}'.format(link))
                    r.sadd(visited_urls, link)
                    yield scrapy.http.Request(url=link, callback=self.parse)
                else:
                    scrapy.log.msg('Domain not in white list {}'.format(link))
                    if not r.sismember(new_domains, self.get_domain(link)):
                        r.sadd(new_domains, self.get_domain(link))
                        scrapy.log.msg('Found new domain {}'.format(self.get_domain(link)))
            else:
                scrapy.log.msg('Already visited {}'.format(link))
