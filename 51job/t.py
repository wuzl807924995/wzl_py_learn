from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from pyquery import PyQuery as pq
import time
import random


def sl():
    time.sleep(random.randint(1,3))

def save_list(l):
    for x in l:
        print(x)

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
                'time':i.children('span.t5').text(),
            }
            yield rs



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
browser=webdriver.Chrome(chrome_options=chrome_options)
# browser=webdriver.Chrome(executable_path="F:\home\selenium\chromedriver.exe",chrome_options=chrome_options)
browser.get('https://search.51job.com/')

# 搜素关键字
searchK_key=browser.find_element_by_xpath('//*[@id="kwdselectid"]')
searchK_key.clear()
searchK_key.send_keys('python')
ActionChains(browser).move_by_offset(200, 100).click().perform()


address=browser.find_element_by_xpath('//*[@id="work_position_input"]')
address.click()
sl()

# 杭州
city=browser.find_element_by_xpath('//*[@id="work_position_click_ip_location_000000_080200"]')
city.click()
sl()

address_save=browser.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]')
address_save.click()
sl()

#按下搜索按钮
btn_submit=browser.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button')
btn_submit.click()
sl()

# 24 以内
key24=browser.find_element_by_link_text('24小时内')
key24.click()
sl()




html = browser.page_source
doc = pq(html)
# 总页码
total_page = doc('#hidTotalPage').attr('value')
# test
total_page=3
l=list(parse_page(html))
save_list(l)

for page in range(1,total_page):
    if page<=total_page:
        browser.find_element_by_xpath('//*[@id="rtNext"]').click()
        # ipt_page=browser.find_element_by_xpath('//*[@id="jump_page"]')
        # ipt_page.clear()
        # ipt_page.send_keys(page)
        # btn_ok=browser.find_element_by_class_name('og_but')
        # btn_ok.click()
        sl()
        html = browser.page_source  
        l=list(parse_page(html))
        save_list(l)




