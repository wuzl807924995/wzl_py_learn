"""
    1.浏览器启动快捷方式后面添加后面的参数然后重启浏览器 --remote-debugging-port=9222
    2.下载浏览器驱动 对应地址 http://chromedriver.storage.googleapis.com/index.html
    3.配置驱动到path,如果不配用注释哪行代码指向驱动位置也行
    4.安装python3 以及相关依赖 （如果有忽略他）    
"""



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from pyquery import PyQuery as pq
import time
import random

import pymongo

from .db import db_utils

BASE_URL='https://search.51job.com/'
SEARCH_KEY='python'

MONGO_COLLECTION = 't_'+SEARCH_KEY


# def slp(func):
#     @functools.wraps(func) 
#     def inner_function(*args,**kwargs):
#         rs=func(*args,**kwargs)
#         time.sleep(random.randint(1,3))
#         return rs
#     return inner_function

def sl():
    time.sleep(random.randint(3,5))


def save_list(l):
    client = db_utils().MONGO_DB
    db=client[MONGO_DB]

    for x in l:
        db[MONGO_COLLECTION].insert(x)


def parse_page(html):
    doc = pq(html)
    rs_list = doc('#resultList div.el').items()
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
            yield rs

def open_browser():
    """
        打开浏览器
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
    # browser=webdriver.Chrome(chrome_options=chrome_options)
    # browser=webdriver.Chrome(executable_path="F:\home\selenium\chromedriver.exe",chrome_options=chrome_options)

    browser=webdriver.Chrome(executable_path="F:\home\chromedriver.exe",chrome_options=chrome_options)
    # browser=webdriver.PhantomJS(executable_path="")
    return browser

def search_val(browser):
    """
        输入关键字
    """
    searchK_key=browser.find_element_by_xpath('//*[@id="kwdselectid"]')
    searchK_key.clear()
    searchK_key.send_keys(SEARCH_KEY)
    ActionChains(browser).move_by_offset(0, 0).click().perform()    

def open_select_address(browser):
    """
        打开选择位置
    """
    address=browser.find_element_by_xpath('//*[@id="work_position_input"]')
    address.click()



def search(browser):
    """
        按下搜索按钮
    """
    btn_submit=browser.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button')
    btn_submit.click()

def search_time(browser):
    """
      24小时内
    """
    key24=browser.find_element_by_link_text('24小时内')
    key24.click()

def all_select_city(browser):
    """
        选择城市
    """
    city=browser.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_080200"]')
    if city:
        cannel=browser.find_element_by_xpath('//*[@id="work_position_click_bottom"]/span[2]')
        cannel.click()
    else: 
        city=browser.find_element_by_xpath('//*[@id="work_position_click_ip_location_000000_080200"]')
        city.click()
        sl()

        address_save=browser.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]')
        address_save.click()

def run():
    browser=open_browser();
    browser.get(BASE_URL)
    sl()

    search_val(browser)
    sl()

    open_select_address(browser)
    sl()

    all_select_city(browser)
    sl()

    search(browser)
    sl()

    search_time(browser)
    sl()

    #开始解析数据
    html = browser.page_source
    doc = pq(html)
    # 总页码
    total_page = doc('#hidTotalPage').attr('value')
    # test
    total_page=int(total_page)
    l=list(parse_page(html))
    save_list(l)

    for page in range(1,total_page):
        if page<=total_page:
            browser.find_element_by_xpath('//*[@id="rtNext"]').click()
            sl()
            # ipt_page=browser.find_element_by_xpath('//*[@id="jump_page"]')
            # ipt_page.clear()
            # ipt_page.send_keys(page)
            # btn_ok=browser.find_element_by_class_name('og_but')
            # btn_ok.click()
            html = browser.page_source  
            l=list(parse_page(html))
            save_list(l)

if __name__ == "__main__":
    run()


