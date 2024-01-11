# -*- encoding: utf-8 -*-
"""
@File   : weibo_top.py
@Time   : 2024/1/2 21:51
@Author : king
@Project : pytest_fortest
"""

import scrapy

from ..items import sweiboItem


class WeiboTopSpider(scrapy.Spider):
    name = 'weibo_top'
    domain = 'https://s.weibo.com'
    start_urls = ['https://s.weibo.com/top/summary?cate=entrank']
    # cates = ['realtimehot']
    cates = ['realtimehot', 'socialevent', 'entrank', 'sport', 'game']
    cookies = {
        '_s_tentry': 'passport.weibo.com',
        'Apache': '2160923397666.412.1703745674190',
        'SINAGLOBAL': '2160923397666.412.1703745674190',
        'ULV': '1703745674195:1:1:1:2160923397666.412.1703745674190:',
        'XSRF-TOKEN': 'VDx1JqiXSrimJyCp_7ITkzT1',
        'UOR': ',,www.baidu.com',
        'login_sid_t': '4734bafd6583dc3113dfe7a45528490f',
        'cross_origin_proto': 'SSL',
        'wb_view_log': '1463*9151.75',
        'PC_TOKEN': '7d614a578b',
        'WBStorage': '267ec170|undefined',
        'SSOLoginState': '1704339358',
        'SUB': '_2A25IklfODeRhGeNG7lIT8CjPwj6IHXVr7tUGrDV8PUJbkNB-LUTEkW1NS1_oSHpe5_Nyu72qLGARiqbz0DYSmTMX',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2TdBo0hVOmGSr6cTSWXkQ5JpX5KzhUgL.Fo-RSK5Eehq01Kz2dJLoIEXLxKqL1hnL1K2LxKBLBonL12BLxKqL1hML1KzLxKML1-2L1hBLxK-L1KeLBKqt',
        'WBPSESS': 'Dt2hbAUaXfkVprjyrAZT_FBdOUymDnwY3cFZT4fpsm_vFTLaVOJKfnikLryFCvr5fS0i11c5lopXALDets8iUwpKHd2Oq-v5Dy-lGvkNvESbEjIut3-yfqvn1nXYB_M5DQWCOwd1r1L6D9h_7TToxf_PUet-uJqK-4b3orw-XaUNjQsLe4VrVKs2XYWd1b3U4ieVoGBgd65R8FWbK5lPhA==',
    }

    headers = {
        'authority': 'weibo.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'client-version': 'v2.44.45',
        # 'cookie': '_s_tentry=passport.weibo.com; Apache=2160923397666.412.1703745674190; SINAGLOBAL=2160923397666.412.1703745674190; ULV=1703745674195:1:1:1:2160923397666.412.1703745674190:; XSRF-TOKEN=VDx1JqiXSrimJyCp_7ITkzT1; UOR=,,www.baidu.com; login_sid_t=4734bafd6583dc3113dfe7a45528490f; cross_origin_proto=SSL; wb_view_log=1463*9151.75; PC_TOKEN=7d614a578b; WBStorage=267ec170|undefined; SSOLoginState=1704339358; SUB=_2A25IklfODeRhGeNG7lIT8CjPwj6IHXVr7tUGrDV8PUJbkNB-LUTEkW1NS1_oSHpe5_Nyu72qLGARiqbz0DYSmTMX; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2TdBo0hVOmGSr6cTSWXkQ5JpX5KzhUgL.Fo-RSK5Eehq01Kz2dJLoIEXLxKqL1hnL1K2LxKBLBonL12BLxKqL1hML1KzLxKML1-2L1hBLxK-L1KeLBKqt; WBPSESS=Dt2hbAUaXfkVprjyrAZT_FBdOUymDnwY3cFZT4fpsm_vFTLaVOJKfnikLryFCvr5fS0i11c5lopXALDets8iUwpKHd2Oq-v5Dy-lGvkNvESbEjIut3-yfqvn1nXYB_M5DQWCOwd1r1L6D9h_7TToxf_PUet-uJqK-4b3orw-XaUNjQsLe4VrVKs2XYWd1b3U4ieVoGBgd65R8FWbK5lPhA==',
        'referer': 'https://weibo.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'server-version': 'v2024.01.03.1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'VDx1JqiXSrimJyCp_7ITkzT1',
    }

    def start_requests(self):
        for cate in self.cates:
            item = sweiboItem()
            item['module'] = cate
            url = f'https://s.weibo.com/top/summary?cate={cate}'
            yield scrapy.Request(url, meta={'item': item})

    def parse(self, response):
        hot_lists = response.css('.td-02') or response.xpath('//*[@class="td-02"]')
        item = response.meta['item']
        for hot in hot_lists:
            new_item = sweiboItem()
            new_item['module'] = item['module']
            new_item['name'] = hot.css(' a::text').get() or hot.xpath(".//a/text()").get()
            new_item['hot'] = hot.css(' span::text').get() or hot.xpath(".//span/text()").get()
            if new_item['hot'] and len(new_item['hot'].split()) >= 1:
                for i in new_item['hot'].split():
                    if i.isdigit():
                        new_item['hot'] = int(i)
                        break
            href_url = hot.css(' a::attr(href)').get() or hot.xpath(".//a/@href").get()
            if "javascript:void(0);" in href_url:
                continue
            hot_search_url = f"https://s.weibo.com{href_url}"
            yield scrapy.Request(hot_search_url, callback=self.parse_hot_search, meta={'item': new_item})

    def parse_hot_search(self, response):
        item = response.meta['item']
        news_list = response.xpath('//div[@action-type="feed_list_item"]')
        for news in news_list:
            new_item = sweiboItem()
            new_item['module'] = item['module']
            new_item['name'] = item['name']
            new_item['hot'] = item['hot']
            new_item['author'] = news.css(' p[node-type="feed_list_content"]::attr(nick-name)').get()
            new_item['author'] = news.xpath('.//p[@node-type="feed_list_content"]/@nick-name').get().strip()
            try:
                new_item['public_time'] = news.xpath('.//div[@class="from"]/a[1]/text()').get().strip()
            except:
                new_item['public_time'] = news.xpath('.//div[@class="from"]/a[1]/text()').get()
            new_item['content'] = "".join(
                map(str.strip, news.xpath('.//p[@node-type="feed_list_content"]/text()').getall()))
            if news.xpath('.//p[@node-type="feed_list_content_full"]/text()').getall():
                new_item['content'] = "".join(
                    map(str.strip, news.xpath('.//p[@node-type="feed_list_content_full"]/text()').getall()))
            new_item['video'] = news.xpath('.//div[@aria-label="视频播放器"]/video/@src').get()
            picture_list = news.xpath('.//div[@class="media media-piclist"]//li')
            new_item['picture'] = []
            if picture_list:
                for picture in picture_list:
                    picture_ = picture.xpath('.//img/@src').get()
                    picture_l = picture_.split('/')
                    picture_l[-2] = 'mw690' if 'jpg' in picture_l[-1] else picture_l[-2]
                    picture_ = '/'.join(picture_l)
                    new_item['picture'].append(picture_)
                    if picture.xpath('.//video/@src').get():
                        new_item['picture'].append(picture.xpath('.//video/@src').get())
            yield new_item
