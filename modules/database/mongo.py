"""

Module for the definition of non sequential database

"""

import pymongo


class MongoDB:

    def __init__(self, database, col, address='127.0.0.1'):  # 'mongodb://localhost:27017/'):
        super(MongoDB, self).__init__()
        self.client = pymongo.MongoClient(address)
        self.database = self.client[database]
        self.collection = self.database[col]

    def sort(self, keyword):
        return self.collection.find().sort(keyword, -1)

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete_many(self, query):
        return self.delete_many(query)

    def delete_all(self):
        return self.collection.delete_many({})

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def find(self, query):
        return self.collection.find(query)  # { keyword : value })

    def find_all(self, keyword=None):
        return self.collection.find()

    def delete_collection(self):
        return self.collection.drop()

    def create_collection(self, name):
        return self.database.create_collection(name=name)

    def test_connection(self, ip_address):
        maxSevSelDelay = 1
        try:
            client = pymongo.MongoClient(ip_address, serverSelectionTimeoutMS=maxSevSelDelay)
            print(client.server_info())
            client.close()
            return True
        except Exception as e:
            print(str(e))
            return False

    def update_connection(self, ip, db, col):
        self.client.close()
        self.client = pymongo.MongoClient(ip, serverSelectionTimeoutMS=2)
        self.database = self.client[db]
        self.collection = self.database[col]
        print(self.client.server_info())







