# -*- coding: utf-8 -*-

import scrapy
from scrapy.http.request import Request
from urllib.parse import quote
from warehouse.utils.common import baikeQueryCompany
import json
from warehouse.utils.HtmlParser import IframeHtmlParser
import os
from warehouse.items import CompanyItem
from warehouse.pipelines import CompanyPipeline


class CompanySpider(scrapy.Spider):
    name = "company"
    pipeline = set([CompanyPipeline])
    allowed_domains = ["*.baidu.com"]
    
    def start_requests(self):
        file = open("%s/companyName" % os.getcwd(), "r")
        for line in file:
            cn = line.strip()
            companies = baikeQueryCompany(cn)
            for s in companies:
                url = "https://baike.baidu.com/wikiui/api/getcertifyinfo?lemma=%s" % quote(s)
                yield Request(url, self.parse)

    def parse(self, response):
        # 兼容3.4
        data = json.loads(response.body.decode("utf-8"))['data']
        item = CompanyItem()
        for i in data:
            if i in item.fields:
                item[i] = data[i]
        
        # 如果有数据则保存，没有则打印
        if 'id' in item.keys():
            yield item
        else:
            print(data)
#         print(data)
        if 'iframe' in data:
            request = Request(url=data['iframe'], callback=self.parse_iframe, dont_filter=True)
            request.meta['PageName'] = data['lemmaTitle']
            yield request

    def parse_iframe(self, response):
        # 这个可以换成xpath或者css选择器来实现
        iframeDataDecode = response.body.decode("utf-8")
        hp = IframeHtmlParser()
        hp.feed(iframeDataDecode)
        hp.close()
#         print("qixinLink: %s" % hp.qixinLink)
        request = Request(url=hp.qixinLink, callback=self.post_qixin, dont_filter=True)
        request.meta['PhantomJS'] = True
        request.meta['PageName'] = response.request.meta['PageName']
        yield request
        
    def post_qixin(self, response):
        file_path = "%s/downloads/html/%s.html" % (os.getcwd(), response.request.meta['PageName'])
#         print(file_path)
        html_file = open(file_path, "+w")
        print(response.body.decode("utf-8"), file=html_file)
        
