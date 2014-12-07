#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import redis


def main():
    pool = redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    r = redis.Redis(connection_pool=self.pool)
    while True:
        item = r.spop("digspider:new_domains")
        try:
            if item:
                print u"Processing: {}".format(item)
        except KeyError:
            print u"Error procesing: {}".format(item)

        time.sleep(5)


if __name__ == '__main__':
    main()
