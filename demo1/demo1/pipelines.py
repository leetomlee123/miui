# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline


class Demo1Pipeline(object):
    def process_item(self, item, spider):
        return item


class MiuiPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            if value:
                image_file_path = value.get("path", "")
            item["image_file_path"] = image_file_path
            return item


class MysqlPoolPipeline(object):
    def __init__(self, dbPool):
        self.dbPool = dbPool

    @classmethod
    def from_settings(cls, settings):
        params = dict(host=settings["HOST"],
                      db=settings["DBNAME"],
                      user=settings["NAME"],
                      passwd=settings["PASSWD"],
                      charset="utf8",
                      cursorclass=MySQLdb.cursors.DictCursor,
                      use_unicode=True,
                      )
        dbPool = adbapi.ConnectionPool("MySQLdb", **params)
        return cls(dbPool)

    def process_item(self, item, spider):
        # 异步插入
        query = self.dbPool.runInteraction(self.db_insert, item)
        query.addErrback(self.errorHandler)

    def errorHandler(self, failure):
        print(failure)

    def db_insert(self, cursor, item):
        sql, params = item.get_insert_sql()
        cursor.execute(sql, params)
