from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import Page, db_connect, create_pages_table


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
        page.charset = item['charset']
        page.content = item['content']
        page.last_crawled = datetime.utcnow()
        page.spider = spider.name

        try:
            session.add(page)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
