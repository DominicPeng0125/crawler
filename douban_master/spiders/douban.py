# -*- coding: utf-8 -*-
import scrapy
import redis
from douban_master.items import DoubanMasterItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    # start_urls = ['http://book.douban.com/']

    def start_requests(self):
        client = redis.StrictRedis(host=self.settings.get('REDIS_HOST'), port=self.settings.get('REDIS_PORT'), db=1)
        while client.llen('book:tag_urls'):
            url = 'https://book.douban.com' + client.lpop('book:tag_urls').decode('utf8')
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        urls = response.css('li.subject-item h2 a::attr(href)').getall()
        for each in urls:
            item = DoubanMasterItem()
            item['url'] = each
            yield item
        next_url = response.css('span.next a::attr(href)').get()
        if next_url:
            yield scrapy.Request(url='https://book.douban.com'+next_url, callback=self.parse, dont_filter=True)
