# -*- encoding: utf-8 -*-
"""
@File   : run.py
@Time   : 2024/1/2 22:03
@Author : king
@Project : pytest_fortest
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time


st = time.time()
# 获取Scrapy项目的设置
settings = get_project_settings()

# 创建CrawlerProcess对象
process = CrawlerProcess(settings)

# 添加要执行的Spider
process.crawl('weibo_top')
# process.crawl(Spider2)

# 启动爬虫
process.start()
print(f'微博热榜爬虫时间 {(time.time()-st)/60} min')
