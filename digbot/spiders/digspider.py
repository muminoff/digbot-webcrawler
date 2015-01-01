# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.markup import remove_tags, remove_tags_with_content
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from digbot.items import PageItem
from digbot import settings
import scrapy
import tldextract
import redis
from bs4 import BeautifulSoup
from urlparse import urlparse


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

    def get_domain_fqdn(self, url):
        ex = tldextract.extract(url)
        empty_subdomain = ex.subdomain == ''
        subdomain_exists = ex.subdomain != None
        if subdomain_exists and not empty_subdomain:
            return "{}.{}".format(ex.subdomain, ex.registered_domain)

        return ex.registered_domain

    def in_root_path(url):
        return urlparse(url).path == '/' or urlparse(url).path == ''

    def looks_like_forum_site(url):
        forum_tags = [
            'forum',
        ]

        for tag in forum_tags:
            if tag in url:
                return True

        return False

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
            soup = BeautifulSoup(response.body)
        except:
            soup = BeautifulSoup(response.body_as_unicode())
        finally:
            for unwanted_tag in soup(["title", "script", "style"]):
                unwanted_tag.extract()
            clean_text = u' '.join(a for a in soup.get_text().split())
            item['content'] = clean_text

        yield item

        r = redis.Redis(connection_pool=self.pool)
        new_domains = self.name + ':new_domains'

        for link in tld_links:
            if self.looks_like_forum_site(link):
                continue
            this_domain = self.get_domain_fqdn(link)
            visited_urls = '{}:{}:visited_urls'.format(self.name, this_domain)
            if not r.sismember(visited_urls, link):
                if self.is_domain_in_white_list(link):
                    scrapy.log.msg('Following link {}'.format(link), level=scrapy.log.INFO)
                    if not self.in_root_path(link):
                        r.sadd(visited_urls, link)
                    yield scrapy.http.Request(url=link, callback=self.parse)
                else:
                    scrapy.log.msg('Domain not in white list {}'.format(this_domain), level=scrapy.log.INFO)
                    if not r.sismember(new_domains, this_domain):
                        r.sadd(new_domains, this_domain)
                        scrapy.log.msg('Found new domain {}'.format(this_domain), level=scrapy.log.INFO)
            else:
                scrapy.log.msg('Already visited {}'.format(link), level=scrapy.log.INFO)
