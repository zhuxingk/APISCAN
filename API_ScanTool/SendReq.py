import requests
from pymongo import MongoClient

# 连接 MongoDB
client = MongoClient('mongodb://localhost:27017')

# 选择数据库
db = client['APIInfo']

# 选择集合
collection = db['APICollection']


def execute_api(url, method, request):
    # 定义支持的方法和对应的请求函数
    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete
    }

    # 检查方法是否支持
    if method not in methods:
        return {'error': f'Unsupported method: {method}'}

    try:
        # 执行请求函数
        response = methods[method](url, json=request)

        return {'status_code': response.status_code, 'response': response.json()}
    except Exception as e:
        return {'error': str(e)}


def execute_all_apis():
    import requests
    from pymongo import MongoClient

    # 连接 MongoDB
    client = MongoClient('mongodb://localhost:27017')

    # 选择数据库
    db = client['APIInfo']

    # 选择集合
    collection = db['APICollection']
    response_collection = db['APIResponse']

    def execute_api(url, method, request):
        # 定义支持的方法和对应的请求函数
        methods = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

        # 检查方法是否支持
        if method not in methods:
            return {'error': f'Unsupported method: {method}'}

        try:
            # 执行请求函数
            response = methods[method](url, json=request)

            return {'status_code': response.status_code, 'response': response.json()}
        except Exception as e:
            return {'error': str(e)}

    def execute_all_apis():
        error_report = []

        # 获取所有接口文档
        docs = collection.find()

        for doc in docs:
            name = doc['name']
            url = doc['URL']
            method = doc['Method']
            request = doc['Request']

            result = execute_api(url, method, request)

            if 'error' in result:
                error_report.append({'name': name, 'url': url, 'error': result['error']})
            else:
                status_code = result['status_code']
                response = result['response']

                # 存储响应到APIResponse集合
                response_collection.insert_one({
                    'name': name,
                    'url': url,
                    'response': response
                })

                # 处理接口响应数据，根据需求进行操作

        if len(error_report) > 0:
            print('Error Report:')
            for error in error_report:
                print(f"Name: {error['name']}, URL: {error['url']}, Error: {error['error']}")
        else:
            print('All APIs executed successfully')

    # 执行所有接口
    execute_all_apis()



