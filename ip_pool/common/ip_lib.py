import redis
from random import choice
import time
import aiohttp
import asyncio
import sys
import requests
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError


class IpLib:
    host='192.168.5.31'
    port=6381
    db=0
    key='ip_t'
    default_score=10
    min_score=8
    test_url='http://www.baidu.com'


    def get_cli(self):
        """
            初始化客户端
        """
        cli=redis.StrictRedis(host=self.host,port=self.port,db=self.db)
        return cli



    def save_ip_port(self,ip_port):
        """
            保存代理
        """
        cli=self.get_cli()
        val={ip_port:self.default_score}
        cli.zadd(self.key,val,nx=True)

    def decrease_ip_port(self,ip_port):
        """
            检测代理有效期
        """
        cli=self.get_cli()
        score=cli.zscore(self.key,ip_port)
        if score<self.min_score:
            cli.zrem(self.key,ip_port)
        else:
            cli.zincrby(self.key,-1,ip_port)    

    def ip_count(self):
        """
            检测代理总数
        """
        cli=self.get_cli()
        return cli.zcard(self.key)       

    def random(self):
        """
            随机获取一个代理
        """
        cli=self.get_cli()    
        l=list(range(self.min_score-1,self.default_score+1))
        while True:
            s=l.pop();
            if s:
                result =cli.zrangebyscore(self.key,s,s)
                if len(result):
                    ip_port= choice(result)
                    # self.decrease_ip_port(ip_port)
                    return ip_port
            else:
                return None        

       

    def check_and_get(self):
        """
            检验代理是否有效
        """
        ip_port=self.random()

        str_ip_port=ip_port
        if isinstance(str_ip_port, bytes):
            str_ip_port = str_ip_port.decode('utf-8')
        real_proxy = 'http://' + str_ip_port
        print('real_proxy:'+str_ip_port)

        proxy_dict={
            'http':real_proxy,
            'https':real_proxy
        }
        try:
            session=requests.Session();
            response=session.get(self.test_url,proxies=proxy_dict,timeout=20)
            if response.status_code in [200,302]:
                return str_ip_port
        except Exception as e:
            print(e)
            self.decrease_ip_port(ip_port)
            return None
