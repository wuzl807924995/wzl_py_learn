#!/usr/bin/python3
 
import pymongo
 
myclient = pymongo.MongoClient('mongodb://192.168.5.173:27017/')
 
dblist = myclient.list_database_names()
# dblist = myclient.database_names() 
if "runoobdb" in dblist:
  print("数据库已存在！")
else:
    print("不存在")    
    