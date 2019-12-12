# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class Book(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    _id = scrapy.Field()
    author = scrapy.Field()
    cover = scrapy.Field()
    bookDesc = scrapy.Field()
    lastUpdate = scrapy.Field()
    lastChapter = scrapy.Field()
    chapterIds = scrapy.Field()

class Chapter(scrapy.Item):
    # define the fields for your item here like:
    # bookId = scrapy.Field()
    content = scrapy.Field()
    name = scrapy.Field()
    _id=scrapy.Field()


class MiuiItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MiuiItem(scrapy.Item):
    front_image_url = scrapy.Field()
    author = scrapy.Field()
    group = scrapy.Field()
    integral = scrapy.Field()
    phoneType = scrapy.Field()
    miuiVersion = scrapy.Field()
    classify = scrapy.Field()
    title = scrapy.Field()
    view_nums = scrapy.Field()
    replies = scrapy.Field()
    content = scrapy.Field()
    image_file_path = scrapy.Field()
    url_object_code = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into miui VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = (
            self["url_object_code"], self["author"], self["group"], self["integral"], self["phoneType"],
            self["miuiVersion"], self["classify"], self["title"], self["view_nums"], self["replies"], self["content"],
            self["image_file_path"])
        return insert_sql,params
