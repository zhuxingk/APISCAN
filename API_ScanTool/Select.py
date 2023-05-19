import argparse

import requests
from pymongo import MongoClient


# 以类的形式实现
class Select:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['APIInfo']
        self.collection = self.db['APICollection']

    def prompt(self, name, url, method, request):
        # 从MongoDB  APIInfo数据库的APICollection集合中获取接口信息，将获取到接口名称作为CLI的选项；
        name = self.collection.find({}, {"name": 1})
        # 统计获取到的接口名称的数量
        # count = self.collection.find({}, {"name": 1}).count()
        # 将获取到的接口名称放入列表中
        name_list = []
        for i in name:
            name_list.append(i["name"])
        # 将获取到的接口名称作为CLI的选项
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', '--name', choices=name_list, help='API name')
        args = parser.parse_args()
        # 根据接口名称获取接口信息
        api_info = self.collection.find_one({"name": args.name}, {"URL": 1, "Method": 1, "Request": 1})
        # 将获取到的接口信息分别赋值给url、method、request
        url = api_info["URL"]
        method = api_info["Method"]
        request = api_info["Request"]
        return url, method, request
    # 调用APISender类的execute_api方法，根据CLI确定的接口，执行对应的接口
    def execute_api(self, url, method, request):
        # 执行单个接口
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
        except Exception as e:
            return {'error': str(e)}





