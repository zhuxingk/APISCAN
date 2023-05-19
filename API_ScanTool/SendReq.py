import requests
from pymongo import MongoClient
from MongoDBClient import MongoDBClient

class APISender:
    # 初始化APISender实例
    def __init__(self, mongodb_client, collection_name=None, response_name=None):
        self.db_collection = mongodb_client.get_collection(collection_name)
        self.db_response = mongodb_client.get_collection(response_name)

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

    # 从MongoDB的APICollection集合中获取所有API的名称
    def get_api_names(self):
        names = []

        docs = self.db_collection.find({}, {"name": 1})
        for doc in docs:
            names.append(doc['name'])

        return names

    def save_response(self, mongodb_client,name, url, method, request, status_code, response):
        # 判断是否已经存在该API的响应数据，如果存在则更新，否则插入
        if self.db_response.find_one({'name': name}):
            self.db_response.update_one(
                {'name': name},
                {'$set': {
                    'url': url,
                    'method': method,
                    'request': request,
                    'status_code': status_code,
                    'response': response
                }}
            )
        else:
            # 遍历返回的响应数据，判断响应数据中的各项参数是否为空，如果该项参数为空则写入None，否则写入响应数据
            for key in response:
                if response[key] is None:
                    response[key] = 'None'
            self.db_response.insert_one(
                {
                    'name': name,
                    'url': url,
                    'method': method,
                    'request': request,
                    'status_code': status_code,
                    'response': response
                }
            )


