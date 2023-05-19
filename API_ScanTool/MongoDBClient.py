from pymongo import MongoClient



class MongoDBClient:
    def __init__(self, mongodb_url, database_name):
        self.client = MongoClient(mongodb_url)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        collection.insert_one(document)

    def update_document(self, collection_name, filter, update):
        collection = self.get_collection(collection_name)
        collection.update_one(filter, update)
