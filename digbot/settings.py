# -*- coding: utf-8 -*-

BOT_NAME = 'digbot'

SPIDER_MODULES = ['digbot.spiders']
NEWSPIDER_MODULE = 'digbot.spiders'

USER_AGENT = 'DigBot'
LOG_LEVEL = 'INFO'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"

CHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

SCHEDULER_IDLE_BEFORE_CLOSE = 10

ITEM_PIPELINES = [
        'scrapy_redis.pipelines.RedisPipeline',
        ]

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
