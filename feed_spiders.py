#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import redis
import sys
from digbot import settings


def main():
    pool = redis.ConnectionPool(
        host='54.172.139.99',
        port=6379,
        db=0
    )
    r = redis.Redis(connection_pool=pool)

    for x in xrange(1, 11):
        domain_name = r.spop('digspider:new_domains')
        try:
            print "Feeding spiders with {} ...".format(domain_name)
            if not r.sismember("digspider:domain_whitelist", domain_name):
                r.sadd("digspider:domain_whitelist", domain_name)
            r.lpush("digspider:start_urls", "http://{}/".format(domain_name))
        except:
            print "Error feeding spiders with {}!".format(domain_name)
            print "Adding {} back to records ...".format(domain_name)
            r.sadd("digspider:new_domains", domain_name)
            break

if __name__ == '__main__':
    main()
