# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):       # 继承scrapy.Item类
    """
    Item是保存爬取数据的容器，使用方法和字典相识，不过比字典多了保护机制，可以避免拼写错误或者定义字段作物。
    """

    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()