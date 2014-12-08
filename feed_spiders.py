#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import redis
import sys


def main():
    if len(sys.argv) < 2:
        print "Usage {} domain.uz".format(sys.argv[0])
        sys.exit(0)

    domain_name = sys.argv[1]

    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    r = redis.Redis(connection_pool=pool)

    try:
        print "Feeding spiders with {} ...".format(domain_name)
        r.sadd("digspider:new_domains", domain_name)
        r.lpush("digspider:start_urls", "http://{}/".format(domain_name))
    except:
        print "Error feeding spiders!"
        sys.exit(-1)

    print "Done"


if __name__ == '__main__':
    main()
