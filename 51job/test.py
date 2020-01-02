import time
from crawler import crawler_51_job

# s='https://jobs.51job.com/all/co2546282.html'

# s='https://jobs.51job.com/hangzhou-fyq/118324989.html?s=01&t=0'

# idx=s.rfind('.html')
# idx2=s.rfind('/')

# idx2+=1

# print(s[idx2:idx])


 
# 格式化成2016-03-20 11:45:39形式
# s=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
# print(s)

c=crawler_51_job();

print(c.run_job_page(c.open_browser(),'https://jobs.51job.com/hangzhou/53313192.html'))