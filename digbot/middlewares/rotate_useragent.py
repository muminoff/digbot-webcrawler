# -*- coding: utf-8 -*- 

import random

from scrapy import log

from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.conf import settings


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        self.user_agent_list = settings['USER_AGENT_LIST']

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            log.msg('Current UserAgent: ' + ua, level=log.INFO)
            request.headers.setdefault('User-Agent', ua)
