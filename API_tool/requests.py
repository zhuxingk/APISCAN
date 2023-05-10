import requests


def select(method):
    # 选择HTTP方法
    if method == "GET":
        print(
            "GET方法：用于请求指定的页面或资源，返回实体主体。GET请求的参数会附加在URL之后，因此GET请求的URL长度会受到限制。GET请求不会改变服务器上的资源。")
        print("适用场景：获取数据。")
    elif method == "POST":
        print("POST方法：用于向指定资源提交数据，请求服务器进行处理（例如提交表单或者上传文件），并返回处理的结果。")
        print("适用场景：提交、新增数据。")
    elif method == "PUT":
        print("PUT方法：用于向指定的URI（统一资源标识符）上传更新资源的内容。")
        print("适用场景：更新数据。")
    elif method == "DELETE":
        print("DELETE方法：用于请求服务器删除指定的页面或资源。")
        print("适用场景：删除数据。")
    elif method == "HEAD":
        print("HEAD方法：类似于GET请求，但是服务器不会返回实体主体部分。")
        print("适用场景：获取头部信息。")
    elif method == "OPTIONS":
        print("OPTIONS方法：用于获取目标资源所支持的通信选项。")
        print("适用场景：查询服务器支持的方法。")
    elif method == "PATCH":
        print("PATCH方法：用于对资源进行部分修改。")
        print("适用场景：更新部分数据。")
    else:
        print("输入的HTTP方法不正确。")


class HttpClient:
    def __init__(self, url: str, method: str = 'GET', headers: dict = None, params: dict = None,
                 data: dict = None, **kwargs):
        """
        初始化请求方法，url，请求头，请求参数，请求体

        :param url: 请求地址
        :param method: 请求方法，支持 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        :param kwargs: 额外的请求参数，如请求超时时间、身份验证、SSL证书验证等
        """
        self.url = url
        self.method = method.upper()  # 统一将请求方法转为大写
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or {}
        self.kwargs = kwargs

    def send_request(self, method: str, url: str, headers: dict = None, params: dict = None,
                     data: dict = None, **kwargs) -> requests.Response:
        """
        发送HTTP/HTTPS请求，并处理响应结果

        :param method: 请求方法，支持 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'
        :param url: 请求地址
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        :param kwargs: 额外的请求参数，如请求超时时间、身份验证、SSL证书验证等
        :return: 响应结果
        """
        method = method.upper()  # 统一将请求方法转为大写
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                **kwargs
            )
            response.raise_for_status()  # 如果响应状态码不是 200，会抛出 HTTPError 异常
            return response
        except requests.RequestException as e:
            print(f"Error occurred while sending request: {e}")

    def get(self, url: str, headers: dict = None, params: dict = None, **kwargs) -> requests.Response:
        """
        发送HTTP GET/PUT/HEAD/OPTIONS/PATCH请求

        :param url: 请求地址
        :param headers: 请求头
        :param params: 请求参数
        :param kwargs: 额外的请求参数，如请求超时时间、身份验证、SSL证书验证等
        :return: 响应结果
        """
        return self.send_request('GET', url, headers=headers, params=params, **kwargs)

    def post(self, headers=None):
        try:
            response = requests.post(
                url=self.url,
                headers=headers or self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def put(self, headers=None):
        try:
            response = requests.put(
                url=self.url,
                headers=headers or self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def delete(self, headers=None):
        try:
            response = requests.delete(
                url=self.url,
                headers=headers or self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def head(self, headers=None):
        try:
            response = requests.head(
                url=self.url,
                headers=headers or self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def options(self, headers=None):
        try:
            response = requests.options(
                url=self.url,
                headers=headers or self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)

    def patch(self, headers=None):
        try:
            response = requests.patch(
                url=self.url,
                headers=headers or self.headers,
                params=self.params,
                data=self.data
            )
            return response
        except Exception as e:
            print(e)
