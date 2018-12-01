# -*- coding: utf-8 -*-
from WeiboSpider.items import WeiboSpiderItem
from scrapy import Request, Spider
import json

class TopicSpider(Spider):
    name = 'weibo_jiaolv'
    start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%23%E7%84%A6%E8%99%91%23&page_type=searchall&page={page}'
    user_url = 'https://weibo.com/u/{uid}'

    def start_requests(self):
        yield Request(self.start_url.format(page=1), callback=self.parse, meta={'page': 1})

    def parse(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
            posts = result.get('data').get('cards')[-1].get('card_group')
            for post in posts:
                weibo_item = WeiboSpiderItem()
                weibo_item['address'] = post.get('scheme')
                mblog = post.get('mblog')
                if mblog:
                    weibo_item['post_time'] = mblog.get('created_at')
                    if mblog.get('isLongText'):
                        weibo_item['content'] = mblog.get('longText').get('longTextContent')
                    else:
                        weibo_item['content'] = mblog.get('text')
                    user = mblog.get('user')
                    if user:
                        uid = user.get('id')
                        weibo_item['user_id'] = uid
                        weibo_item['gender'] = user.get('gender')
                        weibo_item['followers_num'] = user.get('followers_count')
                        weibo_item['follow_num'] = user.get('follow_count')
                        # yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
                yield weibo_item
            page = response.meta.get('page') + 1
            yield Request(self.start_url.format(page=page), callback=self.parse, meta={'page': page})

    def parse_user(self, response):
        print 'sddddddddddddddddddddddd' 
        print response.xpath('//*').extract()
        # weibo_item['birth'] = 
        print response.xpath('//div["detail"]/ul/li[3]/span[-1]/text()').extract()

    def parse_time(self, date):
        if re.match('刚刚', date):
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            minute = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            hour = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
        return date

