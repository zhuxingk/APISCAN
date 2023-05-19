import requests
from pymongo import MongoClient
from logging_manager import LogManager

class Choice:
    def __init__(self, collection_name,  database_name=None):
        logging_manager = LogManager("ch.log")
        logging_manager.log_info("Choice class is initialized")
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]


    def execute_api(self, url, method, request):
        logging_manager = LogManager("ch.log")
        logging_manager.log_info("execute_api method is called")
        methods = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

        if method not in methods:
            logging_manager.log_error(f'Unsupported method: {method}')
            logging_manager.log_info("execute_api method is finished")
            return {'error': f'Unsupported method: {method}'}

        try:
            logging_manager.log_info("execute_api method is finished")
            response = methods[method](url, json=request)
            return {'status_code': response.status_code, 'response': response.json()}
        except requests.exceptions.RequestException as e:
            logging_manager.log_error(str(e))
            logging_manager.log_info("execute_api method is finished")
            return {'error': str(e)}

    def execute_selected_api(self, api_name):
        logging_manager = LogManager("ch.log")
        logging_manager.log_info("execute_selected_api method is called")
        api_info = self.collection.find_one({"name": api_name}, {"URL": 1, "Method": 1, "Request": 1})

        if api_info is None:
            logging_manager.log_error(f'API not found: {api_name}')
            logging_manager.log_info("execute_selected_api method is finished")
            return {'error': f'API not found: {api_name}'}

        url = api_info['URL']
        method = api_info['Method']
        request = api_info['Request']

        return self.execute_api(url, method, request)



