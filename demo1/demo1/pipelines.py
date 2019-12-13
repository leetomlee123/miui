# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.pipelines.images import ImagesPipeline

from demo1.items import Book,Chapter,BidChapId


class Demo1Pipeline(object):
    def process_item(self, item, spider):
        return item
class BookMongoPipeline(object):
    def __init__(self):
        host = '120.27.244.128'
        port = 27017
        dbname = 'biquge'
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        self.mydb = client[dbname]
        # 存放数据的数据库表名


    def process_item(self, item, spider):
        data = dict(item)


        if isinstance(item, Book):
            self.x=self.mydb['book'].insert(data)
        elif isinstance(item,BidChapId):
            self.x=self.mydb['bid_chapid'].insert(data)
        else:
            self.mydb['chapter'].insert(data)

        return item

class BookPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '120.27.244.128',
            'port': 3306,
            'user': 'root',
            'password': '123654789',
            'database': 'book',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        if isinstance(item, Book):
            self.cursor.execute(self.sql, (item['id'],
                                           item['name'], item['cover'], item['bookDesc'], item['author'],
                                           item['lastUpdate'], item['lastChapter']))
            self.conn.commit()

        else:
            self.cursor.execute(self.chaptersql,(item['id'],item['name'],item['bookId'],item['content']))
            self.conn.commit()

        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into book(id,name,cover,bookDesc,author,lastUpdate,lastChapter) values(%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql
    @property
    def chaptersql(self):
        if not self._sql:
            self._sql = """
                insert into chapter(id,name,bookId,content) values(%s,%s,%s,%s)
                """
            return self._sql
        return self._sql


class MiuiPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            if value:
                image_file_path = value.get("path", "")
            item["image_file_path"] = image_file_path
            return item

# class MysqlPoolPipeline(object):
#     def __init__(self, dbPool):
#         self.dbPool = dbPool
#
#     @classmethod
#     def from_settings(cls, settings):
#         params = dict(host=settings["HOST"],
#                       db=settings["DBNAME"],
#                       user=settings["NAME"],
#                       passwd=settings["PASSWD"],
#                       charset="utf8",
#                       cursorclass=MySQLdb.cursors.DictCursor,
#                       use_unicode=True,
#                       )
#         dbPool = adbapi.ConnectionPool("MySQLdb", **params)
#         return cls(dbPool)
#
#     def process_item(self, item, spider):
#         # 异步插入
#         query = self.dbPool.runInteraction(self.db_insert, item)
#         query.addErrback(self.errorHandler)
#
#     def errorHandler(self, failure):
#         print(failure)
#
#     def db_insert(self, cursor, item):
#         sql, params = item.get_insert_sql()
#         cursor.execute(sql, params)
