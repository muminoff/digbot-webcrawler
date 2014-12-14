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
        print "Getting new domains ..."
        members = r.smembers("digspider:new_domains")
        for member in members:
            print member
    except Exception, e:
        print "Error feeding spiders!" + str(e)
        sys.exit(-1)

    print "Done"


if __name__ == '__main__':
    main()
