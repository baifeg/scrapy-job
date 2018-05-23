# coding=utf-8

import urllib.request
from urllib.parse import quote
import time
import sys
import re
import uuid
import json
import functools

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
sysEncode = sys.getfilesystemencoding() 


def baikeQueryCompany(wd):
    now = int(time.time()) * 1000
    array = []
    if wd.endswith("公司"):
        array.append(wd)
    wd = quote(wd)
    url = "https://gsp0.baidu.com/8qUZeT8a2gU2pMbgoY3K/su?wd=%s&prod=baike&_=%d" % (wd, now)
    req = urllib.request.Request(url=url, headers=headers)
    data = urllib.request.urlopen(req).read()
    result = data.decode("gbk")
#     print(result)
    match = re.search("s:\[.*\]", result)
    if(match):
        content = match.group()
        content = content.replace("s:[", "").replace("]", "").replace("\"", "")
        for s in content.split(","):
            if(s.endswith("公司")):
                array.append(s)
    return array


def job51QueryCompany(wd):
    now = int(time.time()) * 1000
    wd = quote(wd)
    url = "http://kwdsrv.51job.com/KwdSrvByKey/default.aspx?src=51jobcompany&kwd=%s&callback=jQuery18308287669922814555_1519632474635&_=%d" % (wd, now)
    req = urllib.request.Request(url=url, headers=headers)
    data = urllib.request.urlopen(req).read()
    result = data.decode("gbk")
    match = re.search("{.*}", result)
    if(match):
        content = match.group()
        jsonObject = json.loads(content)
        content = jsonObject["content"].replace("%", "\\").encode().decode('unicode-escape')
        return content.split("\x009")
    return []

    
def generate_uuid():
    return str(uuid.uuid4())


def check_spider_pipeline(process_item_method):

    def no_operate(self, item, spider):
        return item
    
    @functools.wraps(process_item_method) 
    def wrapper(self, item, spider):
        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)
        if self.__class__ in spider.pipeline:  # 判断要执行的spider中是否包含所需的pipeline　如果有则执行否则抛出DropItem信息
            spider.logger.debug(msg % 'executing')
#             spider.logger.debug("item: %s" % item)
            return process_item_method(self, item, spider)
        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            spider.logger.debug(msg % 'skipping')
            return item

#             raise DropItem("Missing pipeline property")
    return wrapper

# print(job51QueryCompany("广东轩"))
