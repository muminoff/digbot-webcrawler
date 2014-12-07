# -*- coding: utf-8 -*-

BOT_NAME = 'digbot'

SPIDER_MODULES = ['digbot.spiders']
NEWSPIDER_MODULE = 'digbot.spiders'

USER_AGENT = 'DigBot'
LOG_LEVEL = 'DEBUG'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"

SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

SCHEDULER_IDLE_BEFORE_CLOSE = 10

ITEM_PIPELINES = [
    'scrapy_redis.pipelines.RedisPipeline',
    'digbot.pipelines.DigbotPipeline',
]

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'muminoff',
    'password': '',
    'database': 'digspider'
}
