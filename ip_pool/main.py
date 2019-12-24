"""
common  工具类
read_pool 抓取数据
get_pool 读取代理


"""
# from .read_pool.crawler import Crawler
# from .common.ip_lib import IpLib

from read_pool.crawler import Crawler
from common.ip_lib import IpLib

import time
import sys



c=Crawler()
lib=IpLib()

l=list(c.crawl_daili66(1))
for x in l:
    lib.save_ip_port(x)

c=lib.ip_count()

for x in range(0,c*c):
    # c=lib.random()
    c=lib.check_and_get()
    print(c)
    if c:
        if isinstance(c, bytes):
            c = c.decode('utf-8')
        print('yes:'+c)
