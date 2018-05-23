# -*- coding: utf-8 -*-

from sqlalchemy import Column, String , DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from warehouse.utils.common import generate_uuid

Base = declarative_base()

class Job(Base):
    __tablename__ = 'job'
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String) # 职位名称
    source = Column(String) # 数据抓取来源
    source_id = Column(String) # 该记录在数据来源处的ID
    create_time = Column(DateTime) # 记录创建时间
    city = Column(String) # 工作城市
    address = Column(String) # 工作地址
    salary = Column(String) # 月薪
    years_require = Column(String) # 工作年限要求
    degree_require = Column(String) # 学历要求
    amount_require = Column(String) # 招聘人数
    publish_date = Column(Date) # 发布日期
    description = Column(String) # 职位描述
    company_id = Column(String) # 企业ID
    job_category = Column(String) # 职能类别
    department = Column(String) # 部门信息
    update_time = Column(DateTime)#修改时间