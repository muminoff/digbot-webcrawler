# -*- coding: utf-8 -*-
from datetime import datetime


class DigbotPipeline(object):
    def process_item(self, item, spider):
        item["last_crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
