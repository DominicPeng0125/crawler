# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import re


class DoubanMasterPipeline(object):
    def __init__(self, host, port):
        self.r = redis.StrictRedis(host=host, port=port, decode_responses=True, db=1)
        #self.redis_url = 'redis://password:@localhost:6379/'
        #self.r = redis.Redis.from_url(self.redis_url,decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("REDIS_HOST"),
            port=crawler.settings.get("REDIS_PORT"),
        )

    def process_item(self, item, spider):
        bookid = re.findall('/subject/([0-9]+)', item['url'])[0]
        if bookid:
            if self.r.sadd('book:id', bookid):
                self.r.lpush('bookspider:start_urls', item['url'])
        else:
            self.r.lpush('bookspider:no_urls', item['url'])
