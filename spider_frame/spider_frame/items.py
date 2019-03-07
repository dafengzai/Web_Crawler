# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderFrameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_name = scrapy.Field()
    #股票名
    stock_date = scrapy.Field()
    #股票某日期
    stock_date_text = scrapy.Field()
    #股票某日期所对应文本
    pass
