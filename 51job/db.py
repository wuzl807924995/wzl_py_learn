import pymongo
from setting import *

class db_utils(object):


    def get_db(self):
        client = pymongo.MongoClient(host=MONGO_URL,port=MONGO_PORT)
        db=client[MONGO_DB]
        return db