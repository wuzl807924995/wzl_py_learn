import pymongo

class db_utils(object):
    MONGO_URL = '192.168.5.173'
    MONGO_PORT = 27017
    MONGO_DB = 'db_1226'

    def get_db(self):
        client = pymongo.MongoClient(host=MONGO_URL,port=MONGO_PORT)
        db=client[MONGO_DB]
        return db