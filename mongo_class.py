from pymongo import MongoClient
from pprint import pprint

class Mongo_class:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['users']
        self.persons = self.db.persons

    def add_to_db(self, obj: list):
        print("obj")

    def test(self):
        print("Test")

    # for x in many_list:
    #     try:
    #         db.insert_one(x)
    #     except:
    #         duplicatesDB.insert_one(x)

    # for doc in db.find():
    #     print(doc)