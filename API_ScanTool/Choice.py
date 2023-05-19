import requests
from pymongo import MongoClient


class Choice:
    def __init__(self, collection_name,  database_name=None):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]


    def execute_api(self, url, method, request):
        methods = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

        if method not in methods:
            return {'error': f'Unsupported method: {method}'}

        try:
            response = methods[method](url, json=request)
            return {'status_code': response.status_code, 'response': response.json()}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def execute_selected_api(self, api_name):
        api_info = self.collection.find_one({"name": api_name}, {"URL": 1, "Method": 1, "Request": 1})

        if api_info is None:
            return {'error': f'API not found: {api_name}'}

        url = api_info['URL']
        method = api_info['Method']
        request = api_info['Request']

        return self.execute_api(url, method, request)



