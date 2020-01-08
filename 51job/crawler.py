"""
    1.浏览器启动快捷方式后面添加后面的参数然后重启浏览器 --remote-debugging-port=9222
    2.下载浏览器驱动 对应地址 http://chromedriver.storage.googleapis.com/index.html
    3.配置驱动到path,如果不配用注释哪行代码指向驱动位置也行
    4.安装python3 以及相关依赖 （如果有忽略他）    
"""



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pyquery import PyQuery as pq
import time
import random

import pymongo
import sys


class crawler_51_job(object):

    executable_path='F:\home\chromedriver.exe'

    BASE_URL='https://search.51job.com/'
    SEARCH_KEY='java'

    MONGO_URL = '192.168.5.173'
    MONGO_PORT = 27017

    MONGO_DB = 'db_'+time.strftime("%Y%m%d", time.localtime()) 
    MONGO_COLLECTION = 't_'+SEARCH_KEY

    def set_search_key(self,key):
        self.SEARCH_KEY=key
        self.MONGO_COLLECTION='t_'+key

    # def slp(func):
    #     @functools.wraps(func) 
    #     def inner_function(*args,**kwargs):
    #         rs=func(*args,**kwargs)
    #         time.sleep(random.randint(1,3))
    #         return rs
    #     return inner_function

    def sl(self):
        time.sleep(random.randint(3,5))


    def save_list(self,l):
        print('开始保存数据 本次数量：'+str(len(l)))

        client = pymongo.MongoClient(host=self.MONGO_URL,port=self.MONGO_PORT)
        db=client[self.MONGO_DB]

        for x in l:
            db[self.MONGO_COLLECTION].insert(x)


    def parse_page(self,browser,html):
        print('开始解析主页数据')    

        doc = pq(html)
        rs_list = doc('#resultList div.el').items()
        mainWindow = browser.current_window_handle 
        for i in rs_list:
            el_cls=i.attr('class')
            if el_cls=='el':
                rs={
                    'job_name':i.children('p.t1').children('span').children('a').attr('title'),
                    'job_href':i.children('p.t1').children('span').children('a').attr('href'),
                    'company_name':i.children('span.t2').children('a').attr('title'),
                    'company_href':i.children('span.t2').children('a').attr('href'),
                    'company_address':i.children('span.t3').text(),
                    'money':i.children('span.t4').text(),
                    'date':i.children('span.t5').text(),
                    'create_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                }

                job_href=rs['job_href']    
                idx_start=job_href.rfind('/')
                idx_end=job_href.rfind('.html')
                if idx_start!=-1 and idx_end !=-1:
                        rs['job_id']=job_href[idx_start+1:idx_end]

                company_href=rs['company_href']    
                idx_start=company_href.rfind('/')
                idx_end=company_href.rfind('.html')
                if idx_start!=-1 and idx_end !=-1:
                        rs['company_id']=company_href[idx_start+1:idx_end]

                rs['job_detail']=self.run_job_page(browser,rs['job_href'],mainWindow)

                browser.switch_to.window(mainWindow)
                yield rs

    def open_browser(self):
        """
            打开浏览器
        """
        print('开始打开浏览器')    
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        # chrome_options.add_argument('--headless')
        # browser=webdriver.Chrome(chrome_options=chrome_options)
        # browser=webdriver.Chrome(executable_path="F:\home\selenium\chromedriver.exe",chrome_options=chrome_options)

        # browser=webdriver.Chrome(executable_path="F:\home\chromedriver.exe",chrome_options=chrome_options)
        # browser=webdriver.PhantomJS(executable_path=r'C:\Users\John\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')


        browser=webdriver.Chrome(executable_path=self.executable_path,chrome_options=chrome_options)
        return browser

    def search_val(self,browser):
        """
            输入关键字
        """
        print('开始输入关键字:'+self.SEARCH_KEY)    
        searchK_key=browser.find_element_by_xpath('//*[@id="kwdselectid"]')
        searchK_key.clear()
        searchK_key.send_keys(self.SEARCH_KEY)
        ActionChains(browser).move_by_offset(0, 0).click().perform()    

    def open_select_address(self,browser):
        """
            打开选择位置
        """
        print('开始打开定位城市')    
        address=browser.find_element_by_xpath('//*[@id="work_position_input"]')
        address.click()



    def search(self,browser):
        """
            按下搜索按钮
        """
        print('开始搜索')    
        btn_submit=browser.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button')
        btn_submit.click()

    def search_time(self,browser):
        """
        24小时内
        """
        print('开始选择 24小时内')    
        key24=browser.find_element_by_link_text('24小时内')
        key24.click()

    def all_select_city(self,browser):
        """
            选择城市
        """
        print('开始选择城市')    
        city=browser.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_080200"]')
        if city:
            cannel=browser.find_element_by_xpath('//*[@id="work_position_click_bottom"]/span[2]')
            cannel.click()
        else: 
            city=browser.find_element_by_xpath('//*[@id="work_position_click_ip_location_000000_080200"]')
            city.click()
            self.sl()

            address_save=browser.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]')
            address_save.click()


    def run_job_page(self,browser,link,mainWindow):
        """
            新窗口打开页面并爬数据
        """    
        print('开始解析job详细数据:'+link)   

        handles = browser.window_handles
        if len(handles) == 1:
            # 如果只有一个窗口 不抓详细
            return {}


        for h in handles:
            if h != mainWindow:
                browser.switch_to.window(h)


        toHandle  = browser.current_window_handle
        browser.get(link)
        self.sl()

        try:
            html = browser.page_source
            doc = pq(html)
            th_job=doc('div.tHjob')

            page_cn=th_job.children('.in').children('.cn')

            ltype_title=page_cn.children('p.ltype').attr('title')
            msg=ltype_title.replace('\xa0','').replace(' ','').split('|')

            info_job_msg=doc('div.job_msg').text().split('\n')

            rs={
                'title':page_cn.children('h1').attr('title'),
                'money':page_cn.children('strong').text(),
                'address':msg[0],
                'expe':msg[1],
                'schooling':msg[2],
                'num':msg[3].replace('招','').replace('人',''),
                'detail':info_job_msg
            }
            return rs
        except Exception  as e:
            print(e)
            return {}

    def job(self):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def run(self):
        print('开始启动抓包')

        browser=self.open_browser()
        browser.get(self.BASE_URL)
        self.sl()

        self.search_val(browser)
        self.sl()

        self.open_select_address(browser)
        self.sl()

        self.all_select_city(browser)
        self.sl()

        self.search(browser)
        self.sl()

        self.search_time(browser)
        self.sl()

        #开始解析数据
        html = browser.page_source
        doc = pq(html)
        # 总页码
        total_page = doc('#hidTotalPage').attr('value')
        print('数据搜索总页码:'+total_page)   
        total_page=int(total_page)

        print('开始搜索第1页数据')   
        l=list(self.parse_page(browser,html))
        self.save_list(l)

        for page in range(1,total_page):
            if page<=total_page:
                print('开始搜索第'+str((page+1))+'页数据')      

                browser.find_element_by_xpath('//*[@id="rtNext"]').click()
                self.sl()
                # ipt_page=browser.find_element_by_xpath('//*[@id="jump_page"]')
                # ipt_page.clear()
                # ipt_page.send_keys(page)
                # btn_ok=browser.find_element_by_class_name('og_but')
                # btn_ok.click()
                html = browser.page_source  
                l=list(self.parse_page(browser,html))
                self.save_list(l)
