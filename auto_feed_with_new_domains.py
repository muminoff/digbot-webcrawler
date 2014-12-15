#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import redis
import sys
from digbot import settings


def main():
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    r = redis.Redis(connection_pool=pool)

    try:
        print "Getting new domains and feeding spiders ..."
        members = r.smembers("digspider:new_domains")
        for domain_name in members:
            print "Adding {} ...".format(domain_name)
            r.sadd("digspider:domain_whitelist", domain_name)
            r.lpush("digspider:start_urls", "http://{}/".format(domain_name))
    except Exception, e:
        print "Error feeding spiders!" + str(e)
        sys.exit(-1)

    print "Done"


if __name__ == '__main__':
    main()
