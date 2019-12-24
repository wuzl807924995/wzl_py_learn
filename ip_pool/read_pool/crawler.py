import requests
from requests.exceptions import ConnectionError
import json
import re
from pyquery import PyQuery as pq

class Crawler:

    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }

    def get_page(self,url, options={}):
        """
        抓取代理
        :param url:
        :param options:
        :return:
        """
        headers = dict(self.base_headers, **options)
        print('正在抓取', url)
        try:
            response = requests.get(url, headers=headers)
            print('抓取成功', url, response.status_code)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            print('抓取失败', url)
            return None

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = self.get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])