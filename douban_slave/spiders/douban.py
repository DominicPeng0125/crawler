# -*- coding: utf-8 -*-
import scrapy
from douban_slave.items import DoubanSlaveItem
import re
from scrapy_redis.spiders import RedisSpider


class DoubanSpider(RedisSpider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    redis_key = 'bookspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super().__init__(*args, **kwargs)

    def parse(self, response):
        item = DoubanSlaveItem()
        item['id'] = re.findall('/subject/([0-9]+)', response.url)[0]
        item['title'] = response.xpath('//span[@property="v:itemreviewed"]/text()').get()
        item['author'] = '／'.join(response.xpath('//div[@id="info"]//a[contains(@href, "https://book.douban.com/author/") or contains(@href, "/search/")]/text()').getall())
        item['author'] = re.sub('\s', '', item['author'])

        data = response.css('#info').get()
        item['press'] = '，'.join(re.findall('<span class="pl">出版社:</span>([\s\S]*?)<br>', data))
        item['original'] = '，'.join(re.findall('<span class="pl">原作名:</span>([\s\S]*?)<br>', data))
        item['translator'] = '，'.join(re.findall('<span class="pl"> 译者</span>[\s\S]*?<a .*?>(.*?)</a>', data))
        item['imprint'] = '，'.join(re.findall('<span class="pl">出版年:</span>([\s\S]*?)<br>', data))
        item['pages'] = '，'.join(re.findall('<span class="pl">页数:</span>([\s\S]*?)<br>', data))
        item['price'] = '，'.join(re.findall('<span class="pl">定价:</span>([\s\S]*?)<br>', data))
        item['binding'] = '，'.join(re.findall('<span class="pl">装帧:</span>([\s\S]*?)<br>', data))
        item['series'] = '，'.join(re.findall('<span class="pl">丛书:</span>[\s\S]*?<a .*?>(.*?)</a>', data))
        item['isbn'] = '，'.join(re.findall('<span class="pl">ISBN:</span>([\s\S]*?)<br>', data))
        item['score'] = response.css('strong.rating_num::text').get()
        item['number'] = response.xpath('//span[@property="v:votes"]/text()').get()
        for each in item.items():
            if each[1]:
                item[each[0]] = item[each[0]].strip()
        return item

