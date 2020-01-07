from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pyquery import PyQuery as pq
import time
import random

import pymongo

class kdzs(object):
    def sl(self):
        time.sleep(random.randint(3,5))

    def open_browser(self):
        """
            打开浏览器
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        browser=webdriver.Chrome(chrome_options=chrome_options)
        # browser=webdriver.Chrome(executable_path="F:\home\selenium\chromedriver.exe",chrome_options=chrome_options)

        # browser=webdriver.Chrome(executable_path="F:\home\chromedriver.exe",chrome_options=chrome_options)
        # browser=webdriver.PhantomJS(executable_path="")

        browser.implicitly_wait(100)
        return browser

    def open_kdzs(self,browser):
        """
            进入我的应用 快递助手
        """
        base_url='https://www.youzan.com/v4/ump/appcenter-thirdapp/41676'
        #进应用中心
        browser.get(base_url)
        self.sl()


    def goto_kdzs(self,browser):
        """
            跳转进入快递助手 并切换到新页面
        """
        open_use=browser.find_element_by_link_text('去使用')
        open_use.click()

        h = browser.window_handles[-1]
        browser.switch_to.window(h)


    def open_bhd(self,browser):
        """
            打开备货单
        """
        self.sl()
        self.sl()
        bhd=browser.find_element_by_xpath('//*[@id="app-head"]/div/ul/li[5]/a/span')
        bhd.click()

    def search(self,browser):
        """
            开始搜索
        """
        search=browser.find_element_by_xpath('//*[@id="search-bar"]/div/div[2]/a')
        search.click()

        browser.find_element_by_xpath('//*[@id="printTableContent"]')

        
    def parse_page(self,browser,html):
        doc = pq(html)
        rs_list = doc('#printTableContent tbody tr').items()
        for tr in rs_list:
            tds=list(tr.children('td').items())

            if len(tds) > 3:
                rs={
                    'name':tds[1].children('a').text(),
                    'baobei':self.parse_baobei(tds[2]),
                    'count':list(tds[3].children().items())[0].attr('value')
                }

                yield rs

    def parse_baobei(self,td):
        """
            解析我的宝贝
        """
        tx=td.text().replace('\n','').split(':')
        l=list(td.children('span').items())
        idx=0
        all_rs=[]
        for s in l:
           rs={
               'k':tx[idx],
               'v': s.children('input').attr('value')
           }
           idx+=1
           all_rs.append(rs)
        return all_rs

    def save_file(self,list):
        """
            写入我的文件
        """
        f =open(r'C:\Users\wuzl\Desktop\新建文本文档2.txt','w',encoding='utf-8')
        for x in list:
            line=x['name'] + '  总数：'+x['count']+' 详细:'
            line2=''
            for y in x['baobei']:
                line3=y['k']+' 数量：'+y['v']
                line2+=line3
            line+=line2
            line+='\r\n'
            f.write(line)
            print(line)
        f.flush()
        f.close()    

    def run(self,browser):
        html = browser.page_source
        doc = pq(html)
        g=self.parse_page(browser,html)
        rs=list(g)
        self.save_file(rs)


if __name__ == "__main__":
    k=kdzs();
    browser=k.open_browser()

    k.open_kdzs(browser)
    k.goto_kdzs(browser)
    k.open_bhd(browser)
    k.search(browser)

    k.run(browser)