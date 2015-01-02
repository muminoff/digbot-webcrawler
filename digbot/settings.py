# -*- coding: utf-8 -*-
import socket

def is_production():
    return socket.gethostname() != 'blacksmith'

def get_postgre_settings():
    if is_production():
        return {
            'drivername': 'postgres',
            'host': '10.0.1.30',
            'port': '5432',
            'username': 'digmaster',
            'password': 'digmaster',
            'database': 'digdb'
        }

    return {
        'drivername': 'postgres',
        'host': '127.0.0.1',
        'port': '5432',
        'username': 'muminoff',
        'password': '',
        'database': 'digdb'
    }

BOT_NAME = 'digbot'

SPIDER_MODULES = ['digbot.spiders']
NEWSPIDER_MODULE = 'digbot.spiders'

# Commented this line, because we use random user agent since we are getting blocked sometimes ;)
# USER_AGENT = 'DigBot'
LOG_LEVEL = 'ERROR'
# LOG_FILE = './log/digspider.log'

# Broad crawler settings recommendation from scrapy authors
CONCURRENT_REQUESTS = 16
COOKIES_ENABLED = False
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 30
# REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True

SCHEDULER = "scrapy_redis.scheduler.Scheduler" 
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue' 
SCHEDULER_IDLE_BEFORE_CLOSE = 10

ITEM_PIPELINES = {
    'digbot.pipelines.DigbotPipeline':300,
}

USER_AGENT_LIST = [
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'
]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'digbot.middlewares.rotate_useragent.RotateUserAgentMiddleware': 400
}


REDIS_HOST = '10.0.1.20' if is_production() else '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0

DATABASE = get_postgre_settings()
