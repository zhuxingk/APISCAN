import requests


class HttpClient:
    def __init__(self, url, method='GET', headers=None, params=None, data=None):
        # 初始化请求方法，url，请求头，请求参数，请求体
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data

    # 补充使用put和delete方法
    def put(self):
        # 发送put请求
        try:
            response = requests.request(
                method='PUT',
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def delete(self):
        # 发送delete请求
        try:
            response = requests.request(
                method='DELETE',
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def send(self):
        # 发送请求时灵活使用各种请求方法,优先使用get方法，其次使用put和delete方法
        try:
            response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)
