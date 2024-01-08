# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import scrapy
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time, datetime
from jinja2 import Template
from playwright.sync_api import sync_playwright
from scrapy.utils.project import get_project_settings
import cookie
import textwrap


class SweiboSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SweiboDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class PlaywrightMiddleware:
    def __init__(self):
        self.cookies = cookie.cookies
        self.headers = cookie.headers
        self.last_login_time = cookie.last_time

    def process_request(self, request, spider):
        if not self.cookies or not self.headers or self.should_relogin():
            self.login_and_get_cookies()

        request.cookies = self.cookies
        request.headers.update(self.headers)

    def should_relogin(self):
        settings = get_project_settings()
        relogin_interval = settings.get('RELOGIN_INTERVAL', 3600*8)  # 默认为1小时
        current_time = time.time()
        if self.last_login_time is None or current_time - self.last_login_time > relogin_interval:
            return True
        return False

    def login_and_get_cookies(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # 打开微博登录页面
            page.goto('https://weibo.com/login.php')

            # 输入用户名和密码
            page.wait_for_timeout(1000)
            page.fill('#loginname', input())
            page.wait_for_timeout(500)
            page.fill('[type="password"]', input())
            page.fill('#loginname', input())

            # 点击登录按钮
            page.wait_for_timeout(500)
            page.click('[node-type="submitBtn"]')
            code_input = input()
            page.fill('[value="验证码"]', code_input)
            page.click('[node-type="submitBtn"]')

            # 等待登录成功
            page.wait_for_selector('[title=全部关注]')

            # 获取cookies和headers信息
            self.cookies = {cookie['name']: cookie['value'] for cookie in context.cookies()}
            self.headers = {
                'User-Agent': page.evaluate('navigator.userAgent')
            }
            # 更新最后登录时间
            self.last_login_time = time.time()
            f = open('./cookie.py', 'w', encoding='utf-8')
            template = Template(textwrap.dedent("""cookies = {{ cookies }}
            headers = {{ headers }}
            last_time = {{ last_time }}
            
            """))
            f.write(template.render(cookies=self.cookies, headers=self.headers, last_time=self.last_login_time))
            f.close()
            # 关闭浏览器
            browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=scrapy.signals.spider_closed)
        return middleware

    def spider_closed(self, spider):
        self.cookies = None
        self.headers = None
        self.last_login_time = None
