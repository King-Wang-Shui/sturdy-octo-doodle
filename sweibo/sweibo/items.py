# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class sweiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    module = Field()
    name = Field()
    hot = Field()
    author = Field()
    public_time = Field()
    content = Field()
    picture = Field()
    video = Field()



