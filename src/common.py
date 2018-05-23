#!/usr/bin/env python
#coding=utf-8

import urllib.request
from urllib.parse import quote
import time
import sys
import re
import json
from IframeHtmlParser import IframeHtmlParser

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
sysEncode = sys.getfilesystemencoding() 

def queryCompany(wd):
    now = int(time.time()) * 1000
    wd = quote(wd)
    url = "https://gsp0.baidu.com/8qUZeT8a2gU2pMbgoY3K/su?wd=%s&prod=baike&_=%d" % (wd, now)
    req = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(req).read()
    result = data.decode("gbk")
    print(result)
    match = re.search("s:\[.*\]", result)
    if(match):
        content = match.group()
        content = content.replace("s:[", "").replace("]", "").replace("\"", "")
        return content.split(",")
    return []

def info(name):
    name = quote(name)
    url = "https://baike.baidu.com/wikiui/api/getcertifyinfo?lemma=%s" % name
    req = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(req).read()
    return json.loads(data)

def iframeInfo(url):
    req = urllib.request.Request(url=url,headers=headers)  
    data = urllib.request.urlopen(req).read()
    print(data)
    return data;

for s in queryCompany("广东轩辕"):
    data = info("广东轩辕网络科技股份有限公司")[u'data']
    print(data)
    print("regCapital: %s" % data[u'regCapital'])
    print("id: %s" % data[u'id'])
    print("lemmaTitle: %s" % data[u'lemmaTitle'])
    print("lawsuitsCount: %s" % data[u'lawsuitsCount'])
    print("orgType: %s" % data[u'orgType'])
    print("location: %s" % data[u'location'])
    print("qxbUrl: %s" % data[u'qxbUrl'])
    print("scope: %s" % data[u'scope'])
    print("foundTime: %s" % data[u'foundTime'])
    print("belongOrg: %s" % data[u'belongOrg'])
    print("orgCode: %s" % data[u'orgCode'])
    print("termTime: %s" % data[u'termTime'])
    print("noticeCount: %s" % data[u'noticeCount'])
    print("checkDate: %s" % data[u'checkDate'])
    print("changeCount: %s" % data[u'changeCount'])
    print("creditNo: %s" % data[u'creditNo'])
    print("orgRegisterNum: %s" % data[u'orgRegisterNum'])
    print("newLevel: %s" % data[u'newLevel'])
    print("iframe: %s" % data[u'iframe'])
    print("legalPerson: %s" % data[u'legalPerson'])
    print("certStatus: %s" % data[u'certStatus'])
    
    iframeData = iframeInfo(data[u'iframe'])
    iframeDataDecode = iframeData.decode("utf-8")
    print("iframeData: %s" % iframeDataDecode)
    hp = IframeHtmlParser()
    hp.feed(iframeDataDecode)
    hp.close()
    print("qixinLink: %s" % hp.qixinLink)
    
    req = urllib.request.Request(url=hp.qixinLink,headers=headers)  
    data = urllib.request.urlopen(req).read()  
    print(data)
    result = data.decode("utf-8")
    print(result)
    
