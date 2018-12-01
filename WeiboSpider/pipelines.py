# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from WeiboSpider.items import *

class TimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeiboSpiderItem):
            if item.get('created_at'):
                item['post_time'] = item['post_time'].strip()
                item['post_time'] = self.parse_time(item.get('post_time'))
        return item

