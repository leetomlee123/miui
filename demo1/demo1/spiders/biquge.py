# -*- coding: utf-8 -*-
import uuid

from demo1.items import Book, Chapter
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BiqugeSpider(CrawlSpider):
    name = 'Biquge'
    base = 'http://www.xbiquge.la'
    allowed_domains = ['xbiquge.la']
    start_urls = [base]

    rules = (
        Rule(LinkExtractor(allow=r'\d+/\d+/$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        book = Book()
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        book['_id'] = suid
        book['name'] = response.xpath('//*[@id="info"]/h1/text()').extract_first("")
        book['author'] = str(response.xpath('//*[@id="info"]/p[1]/text()').extract_first("")).split('：')[1]
        book['cover'] = response.xpath('//*[@id="fmimg"]/img/@src').extract_first("")
        book['bookDesc'] = response.xpath('//*[@id="intro"]/p[2]/text()').extract_first("")
        book['lastUpdate'] = str(response.xpath('//*[@id="info"]/p[3]/text()').extract_first("")).split('：')[1]
        book['lastChapter'] = response.xpath('//*[@id="info"]/p[4]/a/text()').extract_first("")
        chapterIds = []
        for chapter in response.xpath('//*[@id="list"]/dl/dd'):
            ch_id = str(uuid.uuid4())
            chapter_id = ''.join(ch_id.split('-'))
            chapterIds.append(chapter_id)
            yield Request(self.base + chapter.xpath('a/@href').extract_first(""),
                          meta={'name': chapter.xpath('a/text()').extract_first(""), '_id': chapter_id},
                          callback=self.parseDetail)
        book['chapterIds'] = ','.join(chapterIds)
        yield book

    def parseDetail(self, response):
        chapter = Chapter()
        chapter['name'] = response.meta.get("name", "")
        chapter['_id'] = response.meta.get("_id", "")
        # chapter['bookId'] = response.meta.get("bookId", "")
        contents = ''
        for i in response.xpath('//*[@id="content"]/text()'):
            contents += i.root
        chapter['content'] = contents
        yield chapter
