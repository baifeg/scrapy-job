# -*- coding: utf-8 -*-
from warehouse.config import DBSession
from warehouse.model.company import Company, JobCompany
from scrapy.exceptions import DropItem
from warehouse.config import Redis
from datetime import datetime
from warehouse.utils.common import check_spider_pipeline
from warehouse.items import JobCompanyItem
from warehouse.model.job import Job
from sqlalchemy.sql.functions import func

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CompanyPipeline(object):

    def open_spider(self, spider):
        self._session = DBSession()
        
    @check_spider_pipeline
    def process_item(self, item, spider):
        if Redis.exists('warehouse:company:%s' % item['id']):
            raise DropItem("Duplicate item found: %s" % item['lemmaTitle'])
        entity = Company(
            qxb_id=item['id'],
            create_time=datetime.now(),
            reg_capital=item['regCapital'],
            lemma_title=item['lemmaTitle'],  # 广东轩辕网络科技股份有限公司
            lawsuits_count=item['lawsuitsCount'],  # 2
            org_type=item['orgType'],  # 
            location=item['location'],  # 广州市天河区高普路1033号第8层
            qxb_url=item['qxbUrl'],  # http://www.qixin.com/company/9dcb69a5-fafa-4aae-bd97-f5569d5e3341
            scope=item['scope'],  # 软件开发;计算机网络系统工程服务;计算机技术开发、技术服务;商品批发贸易（许可审批类商品除外）;商品零售贸易（许可审批类商品除外）;软件服务;
            found_time=item['foundTime'],  # 1998年03月02日
            belong_org=item['belongOrg'],  # 广州市工商行政管理局
            org_code=item['orgCode'],  # 708268459
            term_time=item['termTime'],  # 1998年03月02日--
            notice_count=item['noticeCount'],  # 0
            check_date=item['checkDate'],  # 2016年06月28日
            change_count=item['changeCount'],  # 2
            credit_no=item['creditNo'],  # 91440101708268459Q
            org_register_num=item['orgRegisterNum'],  # 440101000085045
            new_level=item['newLevel'],  # 
            level=item['level'],
            legal_person=item['legalPerson'],  # 陈统
            cert_status=item['certStatus'],
        )
        self._session.add(entity)
        self._session.commit()
        Redis.set('warehouse:company:%s' % item['id'], 1)
        
    def close_spider(self, spider):
        self._session.close()


class JobPipeline(object):

    def open_spider(self, spider):
        self._session = DBSession()
        
    @check_spider_pipeline
    def process_item(self, item, spider):
        if isinstance(item, JobCompanyItem):
            self.__process_company_item(item, spider)
        else:
            self.__process_job_item(item, spider)
            
    def __process_company_item(self, item, spider):
        query = self._session.query(JobCompany)
        count = query.filter(JobCompany.name == item['name']).count()
        if count == 0:
            self.__save_company_item(item)
    
    def __save_company_item(self, item):
        entity = JobCompany()
        entity.create_time = datetime.now()
        # TODO refine this
        entity.address = item['address']
        entity.level = item['level']
        entity.name = item['name']
        entity.office_website = item['office_website']
        entity.profile = item['profile']
        entity.scope = item['scope']
        entity.source = item['source']
        entity.source_id = item['source_id']
        entity.staff_scale = item['staff_scale']
        
        self._session.add(entity)
        self._session.commit()
        
    def __process_job_item(self, item, spider):
        count = self._session.query(func.count(Job.id)).filter(Job.source == item['source'], Job.source_id == item['source_id']).scalar()
        if count == 0:
            self.__save_job_item(item)
        else:
            self.__update_job_item(item)
            
    def __save_job_item(self, item):
        query = self._session.query(JobCompany)
        company = query.filter(JobCompany.name == item['company_name']).first()
        entity = Job()
        entity.address = item['address']
        entity.amount_require = item['amount_require']
        entity.city = item['city']
        if company is not None:
            entity.company_id = company.id
        entity.create_time = datetime.now()
        entity.degree_require = item['degree_require']
        entity.department = item['department']
        entity.description = item['description']
        entity.job_category = item['job_category']
        entity.publish_date = item['publish_date']
        entity.salary = item['salary']
        entity.source = item['source']
        entity.source_id = item['source_id']
        entity.title = item['title']
        entity.years_require = item['years_require']
        self._session.add(entity)
        self._session.commit()
        
    def __update_job_item(self, item):
        query = self._session.query(Job)
        entity = query.filter(Job.source == item['source'], Job.source_id == item['source_id']).first()
        entity.address = item['address']
        entity.amount_require = item['amount_require']
        entity.city = item['city']
        entity.degree_require = item['degree_require']
        entity.department = item['department']
        entity.description = item['description']
        entity.job_category = item['job_category']
        entity.publish_date = item['publish_date']
        entity.salary = item['salary']
        entity.source = item['source']
        entity.source_id = item['source_id']
        entity.title = item['title']
        entity.years_require = item['years_require']
        self._session.merge(entity)
        self._session.commit()
        
    def close_spider(self, spider):
        self._session.close()



