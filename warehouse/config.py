# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import redis

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:123456@10.48.26.101:3306/warehouse?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 初始化redis数据库连接
Redis = redis.StrictRedis(host='10.48.26.101', port=6379, db=0)

# 初始化浏览器
__caps = DesiredCapabilities.PHANTOMJS
__caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0"
WebDriver = webdriver.PhantomJS(executable_path=r'D:/programs/phantomjs-2.1.1-windows/bin/phantomjs.exe', desired_capabilities=__caps)
