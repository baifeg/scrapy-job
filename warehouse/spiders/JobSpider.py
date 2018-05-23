# -*- coding: utf-8 -*-

from datetime import date
import re
import scrapy
from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from warehouse.config import WebDriver
from warehouse.items import JobCompanyItem, JobItem
from warehouse.pipelines import JobPipeline


class Job51Spider(scrapy.Spider):
    name = "51job"
    allowed_domains = ["*.51job.com"]
    pipeline = set([JobPipeline])
    
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&funtype=0100%2C2400%2C2500%2C2800%2C2600&industrytype=01%2C39%2C32%2C38%2C31"
        , "http://search.51job.com/jobsearch/search_result.php?fromJs=1&funtype=2700%2C2900%2C2600&industrytype=37%2C02%2C35%2C40&keywordtype=1&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"
    ]

    def parse(self, response):
        driver = WebDriver
        driver.get(response.url)
        content = driver.page_source.encode('utf-8')
        response = HtmlResponse(response.url, encoding='utf-8', body=content)
        pageStr = response.css(".dw_page .p_box .p_wp .p_in >span::text")[0].extract()
        pageNum = int(pageStr[1: pageStr.find("页", 1, len(pageStr))])
        if pageNum - 1 > 0:
            urlss = []
            for i in range(1000):
                js = "document.getElementById('jump_page').value=%d" % (i + 2)
                driver.execute_script(js)
                driver.find_element_by_css_selector(".p_in .og_but").click()
                content = driver.page_source.encode('utf-8')
                sub_response = HtmlResponse(url=response.url, encoding='utf-8', body=content)
                
                main = sub_response.css("div#resultList div.el")
                urls = main.css(".t2 a::attr(href)").extract()
                urlss.append(urls)
           
            for index in range(len(urlss)):
                for url in urlss[index]:
                    try:
                        for obj in self.__parse_by_webdriver(url):
                            yield obj
                    except Exception as error:
                        print("【"+str(index)+"】spirder error: {0}".format(error))
                        continue

    # 有动态分页，需要用到浏览器触发下一页
    def __parse_by_webdriver(self, url):
        driver = WebDriver
        driver.get(url)
        content = driver.page_source.encode('utf-8')
        response = HtmlResponse(url, encoding='utf-8', body=content)
        for obj in self.__parse_company(response, driver):
            yield obj

    def __parse_company(self, response, driver):
        company = JobCompanyItem()
        company['source'] = self.name
        company['name'] = response.css(".tHCop div h1::text").extract()[0]
        print(response.css(".tHCop div h1::text").extract()[0])
        info = response.css(".tHCop div p.ltype::text").extract()
        if len(info) > 0:
            infos = info[0].split("|")
            company['level'] = infos[0].strip()
            company['staff_scale'] = infos[1].strip()
            company['scope'] = infos[2].strip()
        
        source_id = response.css(".tHCop input#hidCOID::attr(value)").extract()
        company['source_id'] = source_id[0] if len(source_id) > 0 else None
        profile = "".join(response.css(".tCompany_full .con_msg p::text").extract()).strip()
        if len(profile) > 5000:
            company['profile'] = profile[0:5000]
        else:
            company['profile'] = profile
        company['address'] = "".join(response.css(".tCompany_full .tBorderTop_box.bmsg div.inbox >p:first-child::text").extract()).strip().replace(' ', '')
        company['office_website'] = "".join(response.css(".tCompany_full .tBorderTop_box.bmsg div.inbox >p:nth-child(3) a::attr(href)").extract())
        yield company
        
        # 抓取第一页的所有职位数据
        for request in self.__parse_jobs(response, company['name']):
            yield request
            
        # 如果有分页，抓取剩余分页的所有职位数据
        page_count = len(response.css(".tCompany_full .dw_page #cpbotton ul li").extract()) - 2
        if page_count > 1:
            for i in range(page_count - 1):
                js = "onPage(%d)" % (i + 1)
                driver.execute_script(js)
#                 driver.find_element_by_css_selector(".tCompany_full .dw_page #cpbotton ul li:nth-child(%d)" % (i+2)).click()
                content = driver.page_source.encode('utf-8')
                sub_response = HtmlResponse(url=response.url, encoding='utf-8', body=content)
                for request in self.__parse_jobs(sub_response, company['name']):
                    yield request
    
    def __parse_jobs(self, response, company_name):
        """
        # 遍历分页所有职位
        """
        job_urls = response.css(".tCompany_full #joblistdata .el >p >a::attr(href)").extract()
        for url in job_urls:
            request = Request(url, self.__parse_detail, dont_filter=True)
            request.meta['CompanyName'] = company_name
            yield request
    
    def __parse_detail(self, response):
        """
        # 抓取单个职位详情数据
        """
        center = response.css("div.tCompany_center")
        item = JobItem()
        item['title'] = center.css("div.tHjob h1::attr(title)").extract()[0]
        item['source'] = self.name
        item['source_id'] = center.css("div.tHjob h1 input#hidJobID::attr(value)").extract()[0]
        item['city'] = center.css("div.tHjob .lname::text").extract()[0]
        item['salary'] = None
        years = response.xpath("//div[@class='tCompany_main']/div/div/div/span[em[@class='i1']]/text()").extract()
        if len(years) > 0:
            match = re.search("[0-9\-]*", years[0])
            if match:
                item['years_require'] = match.group()
            else:
                item['years_require'] = 0
            
        degree = response.xpath("//div[@class='tCompany_main']/div/div/div/span[em[@class='i2']]/text()").extract()
        if len(degree) > 0:
            item['degree_require'] = degree[0]
        else:
            item['degree_require'] = None
            
        amount = response.xpath("//div[@class='tCompany_main']/div/div/div/span[em[@class='i3']]/text()").extract()
        if len(amount) > 0:
            match = re.search("[0-9\-]*", amount[0])
            if match:
                item['amount_require'] = match.group()
            else:
                item['amount_require'] = None
         
        publish_date = response.xpath("//div[@class='tCompany_main']/div/div/div/span[em[@class='i4']]/text()").extract()
        match = re.search("[0-9]{2}-[0-9]{2}", publish_date[0])
        if match:
            this_year = date.today().year
            date_str = match.group().split("-")
            month = int(date_str[0])
            day = int(date_str[1])
            item['publish_date'] = date(this_year, month, day)
            
        item['description'] = "\n".join(response.css(".tCompany_main .job_msg::text").extract()).strip()
        if len(item['description']) == 0:
            item['description'] = "\n".join(response.css(".tCompany_main .job_msg p::text").extract()).strip()
        if len(item['description']) > 10000:
            item['description'] = item['description'][:10000]
        item['company_name'] = response.request.meta['CompanyName']
        item['job_category'] = ",".join(response.css(".tCompany_main .job_msg .fp")[0].css(".el::text").extract()).strip()
        item['address'] = "".join(response.xpath("//div[@class='tBorderTop_box']/div[a[contains(@class,'i_map')]]/p/text()").extract()).strip()
        department = response.xpath("//div[@class='tBorderTop_box']/div[span[contains(text(), '所属部门：')]]/text()").extract()
        if len(department) > 2:
            item['department'] = department[1]
        else:
            item['department'] = None
        yield item
