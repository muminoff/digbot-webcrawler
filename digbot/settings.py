# -*- coding: utf-8 -*-

BOT_NAME = 'digbot'

SPIDER_MODULES = ['digbot.spiders']
NEWSPIDER_MODULE = 'digbot.spiders'

USER_AGENT = 'DigBot'
LOG_LEVEL = 'CRITICAL'
# LOG_FILE = './log/digspider.log'

# Broad crawler settings recommendation from scrapy authors
CONCURRENT_REQUESTS = 16
COOKIES_ENABLED = False
# DOWNLOAD_TIMEOUT = 30
# REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True

SCHEDULER = "scrapy_redis.scheduler.Scheduler" 
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue' 
SCHEDULER_IDLE_BEFORE_CLOSE = 10

ITEM_PIPELINES = [
    # 'scrapy_redis.pipelines.RedisPipeline',
    'digbot.pipelines.DigbotPipeline',
]

REDIS_HOST = '10.0.1.20'
REDIS_PORT = 6379
REDIS_DB = 0


DATABASE = {
    'drivername': 'postgres',
    'host': '10.0.1.30',
    'port': '5432',
    'username': 'digmaster',
    'password': 'digmaster',
    'database': 'digdb'
}
