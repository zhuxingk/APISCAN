import argparse
import requests
from pymongo import MongoClient


class Choice:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['APICollection']

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


class CLI:
    def __init__(self):
        self.sender = APISender('mongodb://localhost:27017', 'APIInfo')

    def run(self):
        name_list = self.get_api_names()
        api_name = self.get_selected_api(name_list)
        if api_name:
            result = self.sender.execute_selected_api(api_name)
            self.process_result(result)

    def get_api_names(self):
        name_list = []
        docs = self.sender.collection.find({}, {"name": 1})
        for doc in docs:
            name_list.append(doc["name"])
        return name_list

    def get_selected_api(self, name_list):
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', '--name', choices=name_list, help='API name')
        args = parser.parse_args()
        return args.name

    def process_result(self, result):
        if 'error' in result:
            print(f"API execution failed. Error: {result['error']}")
        else:
            status_code = result['status_code']
            response = result['response']
            print(f"API executed successfully. Status code: {status_code}")
            print(f"Response: {response}")


cli = CLI()
cli.run()
