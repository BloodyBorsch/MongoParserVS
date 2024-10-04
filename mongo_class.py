from pymongo import MongoClient
from itertools import islice


class Mongo_class:

    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["library"]
        self.books = self.db["books"]

    def add_to_db(self, obj: list):
        for x in obj:
            try:
                self.books.insert_one(x)
            except:
                print("пропуск...")

    def get_from_db(self):
        for doc in self.books.find({}, {"_id": False, "description": False}):
            print(doc) 

    # for doc in db.find():
    #     print(doc)

    # for doc in db.find({"x": {"$gt": 30}}):
    #     print(doc)

    # for doc in db.find({$or: [{"x": value1}, {"y": value2}]}):
    #     print(doc)

    # for doc in db.find({"x": {"$regex": "Y."}}, {"_id": 0}):
    #     print(doc)

    # for doc in db.find({"x": {"$regex": "Y."}}, {"_id": 0}).sort("x", -1):
    #     print(doc)

    # db.update_one({"x": value}, {"$set": {"x": value2}}) - замена значения
    # db.update_one({"x": value}, {"$set": new_dict}) - замена значения

    # db.replace_one({"x": value}, new_dict) - замена значения

    # db.delete_one({"x": value}) - удаление значения
