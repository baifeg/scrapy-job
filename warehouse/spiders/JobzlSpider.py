import scrapy
from scrapy.http.response.html import HtmlResponse

from warehouse.config import WebDriver
from warehouse.items import JobCompanyItem, JobItem
from warehouse.pipelines import JobPipeline


class JobzlSpider(scrapy.Spider):
    name = "zljob"
    allowed_domains = ["*.zhaopin.com"]
    pipeline = set([JobPipeline])
    start_urls = [
        "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&jl=选择地区&sm=0&p=1"
    ]
    
    def parse(self,response):
        driver = WebDriver
        driver.get(response.url)
        content = driver.page_source.encode("utf-8")
        response = HtmlResponse(response.url, encoding='utf-8', body=content)
        #获取分页总数
        pageStr = driver.find_element_by_class_name("pagesnum").get_attribute("onkeypress")
        pageNum = int(pageStr.split(",",3)[2].split(")",2)[0])
        
        if pageNum-1 >0:
            urlss = []
            for i in range(pageNum):
                #修改输入框中的页数
                js = "document.getElementById('goto').value=%d" % ( i + 1 )
                driver.execute_script(js)
                #点击确定按钮，执行分页查询
                driver.find_element_by_class_name("nextpagego-btn").click()
                content = driver.page_source.encode("utf-8")
                subResponse = HtmlResponse(response.url,encoding="utf-8",body=content)
                urls = subResponse.css("#newlist_list_content_table .newlist .zwmc a:nth-child(1)::attr(href)").extract()
                urlss.append(urls)
            
            for index in range(len(urlss)):
                urls = urlss[index]
                for i in range(0,len(urls),2):
                    try:
                        for obj in self.__parse_by_webdriver(urls[i]):
                            yield obj
                    except Exception as error:
                        print("【"+str(i)+"】spirder error: {0}".format(error))
                        continue
                    
    def __parse_by_webdriver(self,url):
        driver = WebDriver
        driver.get(url)  
        content = driver.page_source.encode("utf-8")
        response = HtmlResponse(url, encoding='utf-8', body=content)
        #获取公司信息
        for obj in self.__parse_company(response):
            yield obj
            
    def __parse_company(self,response):
        company = JobCompanyItem()
        company['source'] = self.name
        company["source_id"] = None
        company['name'] = "".join(response.css(".terminalpage-right .company-name-t >a::text").extract()).strip()
        company['staff_scale'] = response.css(".terminal-ul.clearfix.terminal-company.mt20 >li:nth-child(1) >strong::text")[0].extract()
        company['level'] = response.css(".terminal-ul.clearfix.terminal-company.mt20 >li:nth-child(2) >strong::text")[0].extract()
        scope = response.css(".terminal-ul.clearfix.terminal-company.mt20 >li:nth-child(3) >strong >a::text").extract()
        if len(scope) > 0:
            company['scope']  = scope[0]
        else:
            company['scope'] = None
        address = "".join(response.css(".terminal-ul.clearfix.terminal-company.mt20 >li:nth-child(4) >strong::text").extract()).strip()
        if len(address) > 0:
            company['address'] = address[0]
        else:
            company['address'] = "".join(response.css(".terminal-ul.clearfix.terminal-company.mt20 >li:nth-child(5) >strong::text").extract()).strip()
        office_website= response.css(".terminalpage-right .img-border >a:nth-child(1)::attr(href)").extract()
        if len(office_website):
            company['office_website'] = office_website[0]
        else:
            company['office_website'] = None
        profile = "".join(response.css(".tab-cont-box .tab-inner-cont >p::text").extract()).strip()
        if len(profile) >5000:
            company['profile'] = profile[0:5000]
        else:
            company['profile'] = profile
        yield company
        for obj in self.__parse_jobs(response,company['name']):
            yield obj
        
    def __parse_jobs(self,response,companyName):
        moreJobUrl = response.css(".color-blue.fr.see-other-job::attr(href)")[0].extract()
        driver = WebDriver
        driver.get(moreJobUrl)
        content = driver.page_source.encode("utf-8")
        subResponse = HtmlResponse(moreJobUrl,encoding="utf-8",body=content)
        
        mainLeft = subResponse.css(".mainLeft >div >h1").extract()
        if len(mainLeft) > 0:
            for obj in self.__parse_job_details(subResponse,driver,companyName):
                yield obj
        else:
            for obj in self.__parse_job_detail(response,companyName):
                yield obj
    def __parse_job_detail(self,response,companyName):   
        jobItem = JobItem()
        jobItem['company_name'] = companyName
        jobItem['source'] = self.name
        jobItem['department'] = None
        sourceId = response.url.split(".htm")[0].split(".com/")[1]
        jobItem["source_id"] = sourceId
        title = response.css("h1::text").extract()[0]
        if len(title) > 0 :
            jobItem['title'] = title[0]
        else:
            jobItem['title'] = title
      
        jobItem['salary'] = "".join(response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(1) >strong::text")[0].extract()).strip()
        jobItem['city'] = response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(2) >strong >a::text")[0].extract()
#        publish_date = response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(3) >strong >span::text").extract()
#         if len(publish_date):
#             jobItem['publish_date'] = publish_date[0]
#         else:
        jobItem['publish_date'] = None
        jobItem['years_require'] = response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(5) >strong::text")[0].extract()
        jobItem['degree_require'] = response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(6) >strong::text")[0].extract()
        jobItem['amount_require'] = "".join(response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(7) >strong::text")[0].extract()).strip()
        jobItem['job_category'] = response.css(".terminalpage-left .terminal-ul.clearfix >li:nth-child(8) >strong >a::text")[0].extract()
        jobItem['address'] = "".join(response.css(".tab-cont-box .tab-inner-cont >h2::text").extract()[0]).strip()
        description = "".join(response.css(".tab-cont-box .tab-inner-cont >p::text").extract()).strip()
        if len(description) > 5000:
            jobItem['description'] = description[0:5000]
        else:
            jobItem['description'] = description
        yield jobItem
    def __parse_job_details(self,response,driver,companyName):     
        urls = response.css(".positionListContent1 .jobName >a::attr(href)").extract()
        for url in urls:
            driver = WebDriver
            driver.get(url)
            content = driver.page_source.encode("utf-8")
            response = HtmlResponse(url,encoding="utf-8",body=content)
            for obj in self.__parse_job_detail(response,companyName):
                yield obj