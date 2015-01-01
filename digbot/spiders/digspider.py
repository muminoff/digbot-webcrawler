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

    def domain_in_whitelist(self, url):
        r = redis.Redis(connection_pool=self.pool)
        ex = tldextract.extract(url)
        empty_subdomain = ex.subdomain == ''
        subdomain_exists = ex.subdomain != None
        if subdomain_exists and not empty_subdomain:
            domain = "{}.{}".format(ex.subdomain, ex.registered_domain)
        else:
            domain = ex.registered_domain

        return r.sismember(self.name + ':domain_whitelist', domain)

    def get_domain_fqdn(self, url):
        ex = tldextract.extract(url)
        empty_subdomain = ex.subdomain == ''
        subdomain_exists = ex.subdomain != None
        if subdomain_exists and not empty_subdomain:
            return "{}.{}".format(ex.subdomain, ex.registered_domain)

        return ex.registered_domain

    def in_root_path(self, url):
        return urlparse(url).path == '/' or urlparse(url).path == ''

    def looks_like_forum(self, url):
        forum_tags = [ 'forum' ]
        domain = self.get_domain_fqdn(url)

        for tag in forum_tags:
            if tag in domain:
                return True

        return False

    def parse(self, response):
        hxs = scrapy.Selector(response)
        extracted_links = self.link_extractor.extract_links(response)
        page_urls = [
            link.url for link in extracted_links if self.is_domestic(link.url)
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
            soup = hxs.xpath('/html/body/**')
            scrapy.log.msg('Cannot get response body from {}'.format(response.url), level=scrapy.log.INFO)
        finally:
            for unwanted_tag in soup(["title", "script", "style"]):
                unwanted_tag.extract()
            clean_text = u' '.join(a for a in soup.get_text().split())
            item['content'] = clean_text

        yield item

        r = redis.Redis(connection_pool=self.pool)
        new_domains = self.name + ':new_domains'
        forum_sites = self.name + ':forum_sites'

        for link in page_urls:
            this_domain = self.get_domain_fqdn(link)
            visited_urls = '{}:{}:visited_urls'.format(self.name, this_domain)
            if self.looks_like_forum(link):
                scrapy.log.msg('Looks like forum site {}, so ignoring...'.format(link), level=scrapy.log.INFO)
                if not r.sismember(forum_sites, this_domain):
                    r.sadd(forum_sites, this_domain)
                continue
            if not r.sismember(visited_urls, link):
                if self.domain_in_whitelist(link):
                    scrapy.log.msg('Following link {}'.format(link), level=scrapy.log.INFO)
                    if not self.in_root_path(link):
                        scrapy.log.msg('Link is not root {}'.format(link), level=scrapy.log.INFO)
                        r.sadd(visited_urls, link)
                    yield scrapy.http.Request(url=link, callback=self.parse)
                else:
                    scrapy.log.msg('Domain not in white list {}'.format(this_domain), level=scrapy.log.INFO)
                    if not r.sismember(new_domains, this_domain):
                        r.sadd(new_domains, this_domain)
                        scrapy.log.msg('Found new domain {}'.format(this_domain), level=scrapy.log.INFO)
            else:
                scrapy.log.msg('Already visited {}'.format(link), level=scrapy.log.INFO)
