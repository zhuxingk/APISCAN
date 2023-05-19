import requests
from pymongo import MongoClient


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


# 创建APISender实例
sender = APISender('mongodb://localhost:27017', 'APIInfo')

# 执行所有接口
sender.execute_all_apis()
