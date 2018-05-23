# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"
 
obj = webdriver.PhantomJS(executable_path=r'D:/programs/phantomjs-2.1.1-windows/bin/phantomjs.exe', desired_capabilities=caps)
obj.set_page_load_timeout(10)
try:
    obj.get('http://www.qixin.com/company/9dcb69a5-fafa-4aae-bd97-f5569d5e3341?token=08211d4f6b12aa2c2e51e7c6f7f9c8ec&from=bkdt')
    print(obj.page_source.encode("utf-8").decode()) 
except Exception as e:
    print(e)

# browser = webdriver.Firefox(executable_path=r'C:/Program Files/Mozilla Firefox/geckodriver.exe')
# browser.get('http://www.qixin.com/company/9dcb69a5-fafa-4aae-bd97-f5569d5e3341?token=08211d4f6b12aa2c2e51e7c6f7f9c8ec&from=bkdt')
# print(browser.page_source.encode("utf-8").decode()) 