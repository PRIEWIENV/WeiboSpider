# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class WeiboSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = Field()
    user_id = Field()
    user_location = Field()
    user_birth = Field()
    address = Field()
    gender = Field()
    post_time = Field()
    followers_num = Field()
    follow_num = Field()
    pass
