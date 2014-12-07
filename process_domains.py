#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import redis


def main():
    r = redis.Redis()
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
