# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CompanyItem(scrapy.Item):
    regCapital = scrapy.Field() # 6774.000000 万人民币
    id = scrapy.Field() # 9dcb69a5-fafa-4aae-bd97-f5569d5e3341
    lemmaTitle = scrapy.Field() # 广东轩辕网络科技股份有限公司
    lawsuitsCount = scrapy.Field() # 2
    orgType = scrapy.Field() # 
    location = scrapy.Field() # 广州市天河区高普路1033号第8层
    qxbUrl = scrapy.Field() # http://www.qixin.com/company/9dcb69a5-fafa-4aae-bd97-f5569d5e3341
    scope = scrapy.Field() # 软件开发;计算机网络系统工程服务;计算机技术开发、技术服务;商品批发贸易（许可审批类商品除外）;商品零售贸易（许可审批类商品除外）;软件服务;
    foundTime = scrapy.Field() # 1998年03月02日
    belongOrg = scrapy.Field() # 广州市工商行政管理局
    orgCode = scrapy.Field() # 708268459
    termTime = scrapy.Field() # 1998年03月02日--
    noticeCount = scrapy.Field() # 0
    checkDate = scrapy.Field() # 2016年06月28日
    changeCount = scrapy.Field() # 2
    creditNo = scrapy.Field() # 91440101708268459Q
    orgRegisterNum = scrapy.Field() # 440101000085045
    newLevel = scrapy.Field() # 
    level = scrapy.Field()
    iframe = scrapy.Field() # https://baike.qixin.com/?eid=9dcb69a5-fafa-4aae-bd97-f5569d5e3341&token=08211d4f6b12aa2c2e51e7c6f7f9c8ec
    legalPerson = scrapy.Field() # 陈统
    certStatus = scrapy.Field() # 在营（开业）企业
    update_time = scrapy.Field()
class JobCompanyItem(scrapy.Item):
    name = scrapy.Field()
    source = scrapy.Field() # 数据抓取来源
    source_id = scrapy.Field() # 该记录在数据来源处的ID
    address = scrapy.Field() # 企业地址
    office_website = scrapy.Field() # 企业官网地址
    level = scrapy.Field() # 公司类型
    scope = scrapy.Field() # 经营范围
    staff_scale = scrapy.Field() # 员工规模
    profile = scrapy.Field() # 企业简介
    update_time = scrapy.Field()
class JobItem(scrapy.Item):
    id = scrapy.Field()
    source = scrapy.Field() # 数据来源，如：51job, 智联招聘, 拉勾网 等
    source_id = scrapy.Field() # 该数据在源处的ID
    title = scrapy.Field() # 职位名称
    city = scrapy.Field() # 工作地点城市
    address = scrapy.Field() # 工作地点
    salary = scrapy.Field() # 月薪
    years_require = scrapy.Field() # 工作年限要求
    degree_require = scrapy.Field() # 学历要求
    amount_require = scrapy.Field() # 招聘人数
    publish_date = scrapy.Field() # 发布日期
    description = scrapy.Field() # 职位描述
    company_name = scrapy.Field() # 企业ID
    department = scrapy.Field() # 部门信息
    job_category = scrapy.Field() # 职能类别
    update_time = scrapy.Field()
    