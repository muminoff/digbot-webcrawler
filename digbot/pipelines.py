from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Page, db_connect, create_pages_table
from scrapy import log
from base64 import b64encode
from binascii import hexlify


class DigbotPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_pages_table(engine)
        self.Session = sessionmaker(bind=engine) 

    def process_item(self, item, spider):
        session = self.Session()
        page = Page()
        page.url = item['url']
        page.title = item['title']
        page.content = item['content'].encode('utf8')
        page.last_crawled = datetime.utcnow()
        page.spider = spider.name

        try:
            session.add(page)
            session.commit()
        except Exception, e:
            session.rollback()
            log.msg(str(e), level=log.CRITICAL)
        finally:
            session.close()

        return item
