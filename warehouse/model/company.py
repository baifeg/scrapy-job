# -*- coding: utf-8 -*-

from sqlalchemy import Column, String , DateTime
from sqlalchemy.ext.declarative import declarative_base
from warehouse.utils.common import generate_uuid

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id = Column(String, primary_key=True, default=generate_uuid)
    qxb_id = Column(String)
    create_time = Column(DateTime) # 记录创建时间
    reg_capital = Column(String) # 6774.000000 万人民币
    lemma_title = Column(String) # 广东轩辕网络科技股份有限公司
    lawsuits_count = Column(String) # 2
    org_type = Column(String) # 
    location = Column(String) # 广州市天河区高普路1033号第8层
    qxb_url = Column(String) # http://www.qixin.com/company/9dcb69a5-fafa-4aae-bd97-f5569d5e3341
    scope = Column(String) # 软件开发;计算机网络系统工程服务;计算机技术开发、技术服务;商品批发贸易（许可审批类商品除外）;商品零售贸易（许可审批类商品除外）;软件服务;
    found_time = Column(String) # 1998年03月02日
    belong_org = Column(String) # 广州市工商行政管理局
    org_code = Column(String) # 708268459
    term_time = Column(String) # 1998年03月02日--
    notice_count = Column(String) # 0
    check_date = Column(String) # 2016年06月28日
    change_count = Column(String) # 2
    credit_no = Column(String) # 91440101708268459Q
    org_register_num = Column(String) # 440101000085045
    new_level = Column(String) # 
    level = Column(String)
    legal_person = Column(String) # 陈统
    cert_status = Column(String) # 在营（开业）企业
    update_time = Column(DateTime)#修改时间
    
class JobCompany(Base):
    __tablename__ = 'job_company'
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)
    source = Column(String) # 数据抓取来源
    source_id = Column(String) # 该记录在数据来源处的ID
    create_time = Column(DateTime) # 记录创建时间
    address = Column(String) # 企业地址
    office_website = Column(String) # 企业官网地址
    level = Column(String) # 公司类型
    scope = Column(String) # 经营范围
    staff_scale = Column(String) # 员工规模
    profile = Column(String) # 企业简介
    update_time = Column(DateTime)#修改时间