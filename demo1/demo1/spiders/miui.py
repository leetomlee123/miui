# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from demo1.items import MiuiItem, MiuiItemLoader
from scrapy.loader import ItemLoader
import uuid


class MiuiSpider(scrapy.Spider):
    name = 'miui'
    allowed_domains = ['www.miui.com']
    start_urls = ['http://www.miui.com/index.html']

    def parse(self, response):
        articles = response.xpath("//div[@class='article']")
        for link in articles:
            detail_url = link.xpath("h3/a/@href").extract()[0]
            front_image_url = link.xpath("a/img/@src").extract()[0]
            yield Request(detail_url, meta={"front_image_url": front_image_url},
                          callback=self.parseDetail)

        next_page = response.css("div.pages .page_next::attr(href)").extract_first("")
        if next_page:
            yield Request(parse.urljoin(response.url, next_page), callback=self.parse)

    def parseDetail(self, response):
        miuiItem = MiuiItem()
        # front_image_url = response.meta.get("front_image_url", "")
        # author = response.css(".pls.favatar .pi .authi.z a::text").extract_first("")
        # group = response.css(".pls.favatar p em a font::text").extract_first("")
        # integral = response.css(".pls.favatar dl dd a::text").extract_first("")
        # phoneType = response.css("#field_field1_1::text").extract_first("")
        # miuiVersion = response.xpath("//dl[@class='pil cl']//dd[4]/text()").extract_first("")
        # classify = response.css("td.plc h1.ts a::text").extract_first("")
        # title = response.css("td.plc h1.ts #thread_subject::text").extract_first("")
        # view_nums = response.css("span.z.as_views::text").extract_first("")
        # replies = response.css("span.z.as_replies::text").extract_first("")
        # content = ''.join(response.css("td.t_f font::text").extract())
        # item["front_image_url"] = [front_image_url]
        # item["author"] = author
        # item["group"] = group
        # item["integral"] = integral
        # item["phoneType"] = phoneType
        # item["miuiVersion"] = miuiVersion
        # item["classify"] = classify
        # item["title"] = title
        # item["view_nums"] = view_nums
        # item["replies"] = replies
        # item["content"] = content
        # item["url_object_code"] = str(uuid.uuid1()).replace("-", "")
        item_loader = MiuiItemLoader(item=MiuiItem(), response=response)
        item_loader.add_value("front_image_url", [response.meta.get("front_image_url")])
        item_loader.add_css("author", ".pls.favatar .pi .authi.z a::text")
        item_loader.add_css("group", ".pls.favatar p em a font::text")
        item_loader.add_css("integral", ".pls.favatar dl dd a::text")
        item_loader.add_css("phoneType", "#field_field1_1::text")
        item_loader.add_css("classify", "td.plc h1.ts a::text")
        item_loader.add_css("title", "td.plc h1.ts #thread_subject::text")
        item_loader.add_css("view_nums", "span.z.as_views::text")
        item_loader.add_css("replies", "span.z.as_replies::text")
        item_loader.add_css("content", "td.t_f font::text")
        item_loader.add_xpath("miuiVersion", "//dl[@class='pil cl']//dd[4]/text()")
        item_loader.add_value("url_object_code", str(uuid.uuid1()).replace("-", ""))
        miuiItem = item_loader.load_item()
        miuiItem["front_image_url"]=[miuiItem.get("front_image_url","")]
        yield miuiItem
