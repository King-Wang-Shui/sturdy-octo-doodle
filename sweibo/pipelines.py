# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pandas as pd
import datetime
import os
import requests
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import re, time
from .items import sweiboItem


current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class SweiboPipeline:
    def process_item(self, item, spider):
        return item


class SaveToJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open(f'result_{current_time}.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


# class SaveToExcelPipeline:
#     def __init__(self):
#         self.df = pd.DataFrame()
#
#     def process_item(self, item, spider):
#         new_item_dict = dict(item)
#         self.df = self.df.append(new_item_dict, ignore_index=True)
#         return item
#
#     def close_spider(self, spider):
#         self.df.to_excel(filename, index=False, header=True)

class SaveToExcelPipeline:
    def __init__(self):
        self.data = []
        self.result_path = 'spider_result'
        self.filename = f"{self.result_path}/output_update.xlsx"

    def open_spider(self, spider):
        self.data = []
        if not os.path.exists(self.result_path):  # 判断result目录是否存在
            os.makedirs(self.result_path)

    def close_spider(self, spider):
        df = pd.DataFrame(self.data)
        writer = pd.ExcelWriter(self.filename, engine='openpyxl')
        try:
            origin_data = pd.read_excel(self.filename, sheet_name=None, engine='openpyxl')
        except Exception:
            origin_data = {}
        for module in df['module'].unique():
            module_data = df[df['module'] == module]
            # 如果原有的sheet页数据存在，则将其与新数据合并
            if module in origin_data:
                merged_data = pd.concat([origin_data[module], module_data], ignore_index=True)
            else:
                merged_data = module_data
            # 去重并保留最新数据
            deduplicated_df = merged_data.drop_duplicates(keep='last')
            # 将去重后的数据追加写入Excel文件的相应sheet页
            deduplicated_df.to_excel(writer, sheet_name=module, index=False)

        writer.close()

    def process_item(self, item, spider):
        if isinstance(item, sweiboItem):
            if item.get('public_time'):
                item['public_time'] = item['public_time'].strip()
                item['public_time'] = self.parse_time(item.get('public_time'))
            if item.get('picture'):
                image_urls = item.get('picture')
                image_path_list = []
                module_path = f'{self.result_path}/{item['module']}'
                if not os.path.exists(module_path):
                    os.makedirs(module_path)
                # 下载图片并保存到结果列表中
                for image_url in image_urls:
                    response = requests.get(image_url)
                    image_path = (f"{module_path}/image_{item['name']}_"
                                  f"{item['author']}_{image_urls.index(image_url)}.jpg")
                    if 'video' in image_url:
                        image_path = (f"{module_path}/gif_{item['name']}_"
                                      f"{item['author']}_{image_urls.index(image_url)}.mp4")
                    f = open(image_path, "wb")
                    f.write(response.content)
                    f.close()
                    image_path_list.append(image_path)
                item['picture'] = image_path_list
        self.data.append(dict(item))

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
            date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60)) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
        return date
