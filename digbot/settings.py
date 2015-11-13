# -*- coding: utf-8 -*-
import os

BOT_NAME = 'digbot'

SPIDER_MODULES = ['digbot.spiders']
NEWSPIDER_MODULE = 'digbot.spiders'

LOG_LEVEL = 'INFO'
# LOG_FILE = './log/digspider.log'
LOG_STDOUT = True

CONCURRENT_REQUESTS = 16
COOKIES_ENABLED = False
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 30
AJAXCRAWL_ENABLED = True

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
SCHEDULER_IDLE_BEFORE_CLOSE = 10

ITEM_PIPELINES = {
    'digbot.pipelines.DigbotPipeline': 300,
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


REDIS_HOST = os.environ.get('DIGBOTWEBCRAWLER_QM_1_PORT_6379_TCP_ADDR', '127.0.0.1')
REDIS_PORT = os.environ.get('DIGBOTWEBCRAWLER_QM_1_PORT_6379_TCP_PORT', 6379)
REDIS_DB = os.environ.get('DIGBOTWEBCRAWLER_QM_1_DB', 0)

DATABASE = {
    'drivername': 'postgres',
    'host': os.environ.get('DIGBOTWEBCRAWLER_DB_1_PORT_5432_TCP_ADDR', '127.0.0.1'),
    'port': os.environ.get('DIGBOTWEBCRAWLER_DB_1_PORT_5432_TCP_PORT', 5432),
    'username': os.environ.get('DIGBOTWEBCRAWLER_DB_1_ENV_DB_USER', 'diguser'),
    'password': os.environ.get('DIGBOTWEBCRAWLER_DB_1_ENV_DB_PASS', 'diguser'),
    'database': os.environ.get('DIGBOTWEBCRAWLER_DB_1_ENV_DB_NAME', 'digdb')
}
