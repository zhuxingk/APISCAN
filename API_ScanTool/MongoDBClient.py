from pymongo import MongoClient

from logging_manager import LogManager

class MongoDBClient:
    def __init__(self, mongodb_url, database_name):
        logging_manager = LogManager("db.log")
        logging_manager.log_info("MongoDBClient class is initialized")
        self.client = MongoClient(mongodb_url)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        logging_manager = LogManager("db.log")
        logging_manager.log_info("get_collection method is called")
        return self.db[collection_name]

    def insert_document(self, collection_name, document):
        logging_manager = LogManager("db.log")
        logging_manager.log_info("insert_document method is called")
        collection = self.get_collection(collection_name)
        collection.insert_one(document)

    def update_document(self, collection_name, filter, update):
        logging_manager = LogManager("db.log")
        logging_manager.log_info("update_document method is called")
        collection = self.get_collection(collection_name)
        collection.update_one(filter, update)
