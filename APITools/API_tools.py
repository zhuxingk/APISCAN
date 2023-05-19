import argparse
import json
import re
import requests
from pymongo import MongoClient, UpdateOne, InsertOne, UpdateMany
import configparser

class APIStorage:
    # 初始化数据库连接
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    # 批量插入接口信息
    def bulk_write_documents(self, operations):
        if operations:
            try:
                result = self.collection.bulk_write(operations)
                print('Number of modified documents:', len(result.upserted_ids) + len(result.modified_ids))
            except Exception as e:
                print('Error occurred while performing bulk write:', e)

    def create_indexes(self):
        try:
            self.collection.create_index('name')
            self.collection.create_index('URL')
            self.collection.create_index('Method')
            self.collection.create_index('response(true)')
            self.collection.create_index('response(false)')
            self.collection.create_index('Extensions')
            print('Indexes created successfully')
        except Exception as e:
            print('Error occurred while creating indexes:', e)

    @staticmethod
    def read_interface_data_from_config(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        field_mapping = {
            'name': 'name',
            'URL': 'URL',
            'Method': 'Method',
            'Request': 'Request',
            'Response(TRUE)': 'Response(TRUE)',
            'Response(FALSE)': 'Response(FALSE)',
            'Extensions': 'Extensions'
        }

        interface_data_list = []

        for section in config.sections():
            if re.match('API', section):
                interface_data = {field: config.get(section, field_mapping[field]) for field in field_mapping}

                for key in ['Request', 'Response(TRUE)', 'Response(FALSE)', 'Extensions']:
                    if key in interface_data:
                        interface_data[key] = json.loads(interface_data[key])

                interface_data_list.append(interface_data)

        return interface_data_list

class APISender:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['APICollection']
        self.response_collection = self.db['APIResponse']
        self.error_collection = self.db['ReqErr']

    def execute_api(self, url, method, request):
        methods = {'GET': requests.get, 'POST': requests.post, 'PUT': requests.put, 'DELETE': requests.delete}

        if method not in methods:
            return {'error': f'Unsupported method: {method}'}

        try:
            response = methods[method](url, json=request)
            return {'status_code': response.status_code, 'response': response.json()}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

    def execute_all_apis(self):
        error_report = []

        interfaces = self.collection.find()

        for interface in interfaces:
            name = interface['name']
            url = interface['URL']
            method = interface['Method']
            request = interface['Request']

            result = self.execute_api(url, method, request)

            if 'error' in result:
                error_report.append({'name': name, 'url': url, 'error': result['error']})
            else:
                status_code = result['status_code']
                response = result['response']

                self.response_collection.insert_one({
                    'name': name,
                    'url': url,
                    'method': method,
                    'request': request,
                    'status_code': status_code,
                    'response': response
                })

        if error_report:
            self.error_collection.insert_many(error_report)

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

        apisender = APISender(mongodb_uri, database_name)
        result = apisender.execute_api(url, method, request)

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
        parser.add_argument('api_name', nargs='?', help='Name of the API to execute')

        args = parser.parse_args()

        if args.api_name:
            result = self.choice.execute_api(args.api_name)

            if 'error' in result:
                print(f'Error occurred: {result["error"]}')
            else:
                self.process_result(result)
        else:
            apisender = APISender(mongodb_uri, database_name)
            apisender.execute_all_apis()

    @staticmethod
    def process_result(result):
        print('Status Code:', result['status_code'])
        print('Response:')
        print(json.dumps(result['response'], indent=2))

class APITester:
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.response_collection = self.db['APIResponse']

    def get_response_info(self):
        return list(self.response_collection.find())

    @staticmethod
    def compare_responses(response_list):
        total_tests = len(response_list)
        passed_tests = 0

        for response in response_list:
            status_code = response['status_code']
            expected_response_true = response['response(true)']
            expected_response_false = response['response(false)']
            actual_response = response['response']

            if status_code == 200:
                if actual_response == expected_response_true:
                    passed_tests += 1
                    print(f'API "{response["name"]}" passed')
                else:
                    print(f'API "{response["name"]}" failed')
            else:
                if actual_response == expected_response_false:
                    passed_tests += 1
                    print(f'API "{response["name"]}" passed')
                else:
                    print(f'API "{response["name"]}" failed')

        print(f'Total tests: {total_tests}, Passed tests: {passed_tests}, Failed tests: {total_tests - passed_tests}')

    @staticmethod
    def get_errormsg(response):
        return response.get('error')

if __name__ == '__main__':
    mongodb_uri = 'mongodb://localhost:27017'
    database_name = 'APIInfo'

    storage = APIStorage(mongodb_uri, database_name)

    # Fix logical issues and optimize
    storage.create_indexes()

    # Read interface data from the configuration file
    interface_data = storage.read_interface_data_from_config('config.ini')

    operations = []

    for data in interface_data:
        name = data['name']
        url = data['URL']
        method = data['Method']
        request = data['Request']
        response_true = data['Response(TRUE)']
        response_false = data['Response(FALSE)']
        extensions = data['Extensions']

        operation = UpdateOne({'name': name}, {'$set': {
            'name': name,
            'URL': url,
            'Method': method,
            'Request': request,
            'Response(TRUE)': response_true,
            'Response(FALSE)': response_false,
            'Extensions': extensions
        }}, upsert=True)

        operations.append(operation)

    # Fix the code while ensuring the existing functionality works
    storage.bulk_write_documents(operations)

    tester = APITester(mongodb_uri, database_name)
    response_info = tester.get_response_info()
    tester.compare_responses(response_info)
