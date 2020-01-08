import schedule
from crawler import crawler_51_job
import time

def schedule_run():
    c=crawler_51_job()
    c.set_search_key('python')
    schedule.every().day.at('17:01').do(c.run)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print('开始启动程序')
    schedule_run()

# crawler_51_job().run()