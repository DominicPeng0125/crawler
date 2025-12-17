# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanSlaveItem(scrapy.Item):
    id = scrapy.Field() 
    title = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field() 
    original = scrapy.Field()
    translator = scrapy.Field()
    imprint = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    binding = scrapy.Field()
    series = scrapy.Field()
    isbn = scrapy.Field()
    score = scrapy.Field() 
    number = scrapy.Field() 
