from crawler import crawler_51_job
import schedule
import time

import argparse
import sys

def run_one():
    keys=['python','java']

    c=crawler_51_job()
    for k in keys:
        c.set_search_key(k)
        c.run()

def schedule_run(t):
    schedule.every().day.at(t).do(run_one)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print(sys.argv)

    print('开始启动程序')
    # schedule_run()
    run_one()
