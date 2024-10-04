from itertools import islice
from mongo_class import Mongo_class

def Start():
    db = Mongo_class()
    db.test()


if __name__ == "__main__":
    Start()