# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):
    def __init__(self):
        self.limit = 50     # 限制长度为50

    def process_item(self, item, spider):
        if item['text']:    # 判断item的text属性是否存在
            if len(item['text']) > self.limit:      # 如果item的text属性长度大于50，则截断然后拼接省略号
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        这是一个类方法，用@classmethod标识，是一种依赖注入的方法，这个方法主要用来获取settings.py中的配置
        :param crawler: 获取全局配置中的每个配置信息
        :return:
        """
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB')
                   )

    def open_spider(self, spider):
        """
        当spider开启时，这个方法会被调用，主要是进行一些初始化操作
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        数据插入操作
        :param item:
        :param spider:
        :return:
        """
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """
        当spider关闭时，这个方法会被调用，这里会关闭数据库链接
        :param spider:
        :return:
        """
        self.client.close()
