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
        book['id'] = suid
        book['name'] = response.xpath('//*[@id="info"]/h1/text()').extract_first("")
        book['author'] = response.xpath('//*[@id="info"]/p[1]/text()').extract_first("")
        book['cover'] = response.xpath('//*[@id="fmimg"]/img/@src').extract_first("")
        book['bookDesc'] = response.xpath('//*[@id="intro"]/p[2]/text()').extract_first("")
        book['lastUpdate'] = response.xpath('//*[@id="info"]/p[3]/text()').extract_first("")
        book['lastChapter'] = response.xpath('//*[@id="info"]/p[4]/a/text()').extract_first("")
        yield book
        for chapter in response.xpath('//*[@id="list"]/dl/dd'):
            yield Request(self.base + chapter.xpath('a/@href').extract_first(""),
                          meta={'name': chapter.xpath('a/text()').extract_first(""), 'bookId': suid},
                          callback=self.parseDetail)


    def parseDetail(self, response):
        chapter = Chapter()
        chapter['name'] = response.meta.get("name", "")
        chapter['bookId'] = response.meta.get("bookId", "")
        contents=''
        for i in response.xpath('//*[@id="content"]/text()'):
            contents+=i.root
        chapter['content'] =contents
        yield chapter
