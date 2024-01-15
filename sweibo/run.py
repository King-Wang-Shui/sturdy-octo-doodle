from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import time
from twisted.internet import reactor
import threading


def run_spider():
    st = time.time()
    # 获取Scrapy项目的设置
    settings = get_project_settings()
    # 创建CrawlerRunner对象
    runner = CrawlerRunner(settings)
    # 添加要执行的Spider
    runner.crawl('weibo_top')
    # 启动爬虫
    # 启动爬虫任务
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    # 开始事件循环
    reactor.run()
    print(f'微博热榜爬虫时间 {(time.time() - st) / 60} min')


# def stop_spider():
#     scheduler.shutdown()
#     print("爬虫任务已停止")


if __name__ == '__main__':
    # import logging
    #
    # # 配置日志记录
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    # logging.getLogger('apscheduler.executors.default').setLevel(logging.INFO)
    #
    # # 创建调度器
    # scheduler = BlockingScheduler()
    #
    # # 定义任务开始时间
    # start_time = "8:00"
    # # 定义任务结束时间
    # end_time = "0:00"
    #
    # # 添加定时任务
    # scheduler.add_job(run_spider, 'interval', hours=1)
    # scheduler.add_job(stop_spider, 'cron', day_of_week='*', hour='0', minute='0')
    #
    # # 启动调度器
    # scheduler.start()
    run_spider()
