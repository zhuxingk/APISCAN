from pymongo import MongoClient
from configparser import ConfigParser
import requests
import argparse
import json

class APIStorage:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['APICollection']

    def create_indexes(self):
        self.collection.create_index('name', unique=True)

    def read_interface_data_from_config(self, config_file):
        config = ConfigParser()
        config.read(config_file)

        interface_data = []

        for section in config.sections():
            data = {
                'name': section,
                'URL': config.get(section, 'URL'),
                'Method': config.get(section, 'Method'),
                'Request': config.get(section, 'Request'),
                'Response(TRUE)': config.get(section, 'Response(TRUE)'),
                'Response(FALSE)': config.get(section, 'Response(FALSE)'),
                'Extensions': config.get(section, 'Extensions')
            }

            interface_data.append(data)

        return interface_data

    def bulk_write_documents(self, operations):
        self.collection.bulk_write(operations)


class APISender:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['APICollection']

    def execute_all_apis(self):
        interfaces = self.collection.find()

        for interface in interfaces:
            url = interface['URL']
            method = interface['Method']
            request = interface['Request']

            response = self.execute_api(url, method, request)
            self.save_response(interface['_id'], response)

    def execute_api(self, url, method, request):
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=request)
            else:
                return {'error': f'Invalid HTTP method: {method}'}

            status_code = response.status_code
            response_data = response.json()

            return {'status_code': status_code, 'response': response_data}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def save_response(self, interface_id, response):
        self.db['APIResponse'].update_one({'_id': interface_id}, {'$set': {'response': response}}, upsert=True)


class Choice:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['APICollection']

    def execute_api(self, name):
        interface = self.collection.find_one({'name': name})

        if not interface:
            return {'error': f'API "{name}" not found'}

        url = interface['URL']
        method = interface['Method']
        request = interface['Request']

        sender = APISender(mongodb_uri, database_name)
        result = sender.execute_api(url, method, request)

        if 'error' in result:
            return {'error': result['error']}
        else:
            status_code = result['status_code']
            response = result['response']

            return {'status_code': status_code, 'response': response}


class CLI:
    def __init__(self, mongodb_uri, database_name):
        self.choice = Choice(mongodb_uri, database_name)

    def run(self):
        parser = argparse.ArgumentParser(description='Execute API by name')
        parser.add_argument('api_name', type=str, help='Name of the API to execute')
        args = parser.parse_args()

        api_name = args.api_name
        result = self.choice.execute_api(api_name)

        if 'error' in result:
            print(f'API execution failed. Error: {result["error"]}')
        else:
            status_code = result['status_code']
            response = result['response']

            print(f'API executed successfully. Status code: {status_code}')
            print(f'Response: {json.dumps(response)}')


class APITester:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.api_collection = self.db['APICollection']
        self.api_response = self.db['APIResponse']

    def get_response_info(self):
        response_true = self.api_collection.find({}, {"Response(TRUE)": 1})
        response_false = self.api_collection.find({}, {"Response(FALSE)": 1})
        api_response = self.api_response.find({}, {"response": 1})
        return response_true, response_false, api_response

    def compare_responses(self, response_info):
        response_true, response_false, api_response = response_info

        for api in response_true:
            error_code = api["Response(TRUE)"].get("errorcode")
            if error_code == 0:
                print(f"API {api['_id']} test successful.")
            else:
                error_msg = self.get_error_msg(api_response, api["_id"])
                print(f"API {api['_id']} test failed. Error message: {error_msg}")

        for api in response_false:
            error_code = api["Response(FALSE)"].get("errorcode")
            if error_code == 0:
                print(f"API {api['_id']} test successful.")
            else:
                error_msg = self.get_error_msg(api_response, api["_id"])
                print(f"API {api['_id']} test failed. Error message: {error_msg}")

    def get_error_msg(self, api_response, api_id):
        response = api_response.find_one({"_id": api_id}, {"response": 1})
        return response["response"].get("errormsg", "")


if __name__ == '__main__':
    mongodb_uri = 'mongodb://localhost:27017'
    database_name = 'APIInfo'

    storage = APIStorage(mongodb_uri, database_name)
    storage.create_indexes()

    interface_data_list = storage.read_interface_data_from_config('config.ini')
    storage.bulk_write_documents(interface_data_list)

    sender = APISender(mongodb_uri, database_name)
    sender.execute_all_apis()

    cli = CLI(mongodb_uri, database_name)
    cli.run()

    tester = APITester(mongodb_uri, database_name)
    response_info = tester.get_response_info()
    tester.compare_responses(response_info)
