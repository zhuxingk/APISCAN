import argparse
import json
import re

import requests
from pymongo import MongoClient
from pymongo import InsertOne, UpdateMany
import configparser

class APIStorage:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def bulk_insert_interfaces(self, interface_data_list):
        if len(interface_data_list) > 0:
            try:
                result = self.collection.insert_many(interface_data_list)
                print('Number of inserted documents:', len(result.inserted_ids))
            except Exception as e:
                print('Error occurred while bulk inserting interface information:', e)

    def bulk_update_interfaces(self, update_data_list):
        try:
            bulk_operations = [UpdateMany({'name': data['name']}, {'$set': data}, upsert=True) for data in update_data_list]
            self.collection.bulk_write(bulk_operations)
            print('接口信息已批量更新')
        except Exception as e:
            print('批量更新接口信息时出错:', e)

    def create_indexes(self):
        try:
            self.collection.create_index('name')
            self.collection.create_index('URL')
            self.collection.create_index('Method')
            self.collection.create_index('response(true)')
            self.collection.create_index('response(false)')
            self.collection.create_index('Extensions')
            print('索引已创建')
        except Exception as e:
            print('创建索引时出错:', e)

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
                # 读取接口信息，初始化为字典
                interface_data = {}

                for field in field_mapping:
                    interface_data[field] = config.get(section, field_mapping[field])

                # Convert JSON strings to Python dictionaries
                for key in ['Request', 'Response(TRUE)', 'Response(FALSE)', 'Extensions']:
                    # 如果接口信息中包含该字段，则将其转换为字典
                    if key in interface_data:
                        interface_data[key] = json.loads(interface_data[key])

                interface_data_list.append(interface_data)

        return interface_data_list
class APISender:
    # 初始化APISender实例
    def __init__(self, mongodb_uri, database_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db['APICollection']
        self.response_collection = self.db['APIResponse']
        self.error_collection = self.db['ReqErr']

    # 执行单个接口
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
        except requests.exceptions.ConnectionError as e:
            return {'error': f'Connection error: {e}'}
        except ValueError as e:
            return {'error': f'Value error: {e}'}

    # 执行所有接口
    def execute_all_apis(self):
        error_report = []

        docs = self.collection.find()  # 使用find方法获取所有文档

        for doc in docs:
            name = doc['name']
            url = doc['URL']
            method = doc['Method']
            request = doc['Request']

            result = self.execute_api(url, method, request)

            if 'error' in result:
                error_report.append({'name': name, 'url': url, 'error': result['error']})
            else:
                status_code = result['status_code']
                response = result['response']

                # 将结果插入数据库之前提取status_code和response
                self.response_collection.insert_one({
                    'name': name,
                    'url': url,
                    'method': method,
                    'request': request,
                    'status_code': status_code,
                    'response': response
                })

        if error_report:
            print('Error Report:')
            for error in error_report:
                print(f"Name: {error['name']}, URL: {error['url']}, Error: {error['error']}")
                self.error_collection.insert_one({
                    'name': error['name'],
                    'url': error['url'],
                    'error': error['error']
                })
        else:
            print('All APIs executed successfully')

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


# 用于测试接口的类
class APITester:
    # 初始化APITester实例
    def __init__(self, mongodb_uri, db_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.api_collection = self.db.APICollection
        self.api_response = self.db.APIResponse
    # 获取所有接口的信息
    def get_response_info(self):
        response_true = self.api_collection.find({}, {"Response(TRUE)": 1})
        response_false = self.api_collection.find({}, {"Response(FALSE)": 1})
        api_response = self.api_response.find({}, {"response": 1})
        return response_true, response_false, api_response
    # 比较接口的响应
    def compare_responses(self):
        response_true, response_false, api_response = self.get_response_info()
        # 遍历所有接口
        for api in response_true:
            errorcode = api["Response(TRUE)"].get("errorcode")
            if errorcode == 0:
                print(f"API {api['_id']} test successful.")
            else:
                errormsg = self.get_errormsg(api_response, api["_id"])
                print(f"API {api['_id']} test failed. Error message: {errormsg}")
        # 遍历所有接口
        for api in response_false:
            errorcode = api["Response(FALSE)"].get("errorcode")
            if errorcode == 0:
                print(f"API {api['_id']} test successful.")
            else:
                errormsg = self.get_errormsg(api_response, api["_id"])
                print(f"API {api['_id']} test failed. Error message: {errormsg}")
    # 获取错误信息
    def get_errormsg(self, api_response, api_id):
        response = api_response.find_one({"_id": api_id}, {"response": 1})
        return response["response"].get("errormsg", "")

if __name__ == '__main__':
    sender = APISender('mongodb://localhost:27017', 'APIInfo')
    sender.execute_all_apis()
    choice = Choice('mongodb://localhost:27017', 'APIInfo')
    result = choice.execute_selected_api('GetAllUsers')
    print(result)
    cli = CLI()
    cli.run()
    tester = APITester('mongodb://localhost:27017', 'APIInfo')
    tester.compare_responses()
