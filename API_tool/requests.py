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


class RequestModule:
    def __init__(self, url: str, method: str = 'GET', headers: dict = None, params: dict = None,
                 data: dict = None, timeout: float = 30, **kwargs):
        """
        初始化请求方法，url，请求头，请求参数，请求体

        :param url: 请求地址
        :param method: 请求方法，支持 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        :param timeout: 请求超时时间
        :param kwargs: 额外的请求参数，如身份验证、SSL证书验证等
        """
        self.url = url
        self.method = method.upper()  # 统一将请求方法转为大写
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or {}
        self.timeout = timeout
        self.kwargs = kwargs

    def send(self):
        """
        发送请求并返回响应

        :return: 响应对象
        """
        response = requests.request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def get(self):
        """
        发送GET请求并返回响应

        :return: 响应对象
        """
        response = requests.get(
            url=self.url,
            headers=self.headers,
            params=self.params,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def post(self):
        """
        发送POST请求并返回响应

        :return: 响应对象
        """
        response = requests.post(
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def put(self):
        """
        发送PUT请求并返回响应

        :return: 响应对象
        """
        response = requests.put(
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def delete(self):
        """
        发送DELETE请求并返回响应

        :return: 响应对象
        """
        response = requests.delete(
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def head(self):
        """
        发送HEAD请求并返回响应

        :return: 响应对象
        """
        response = requests.head(
            url=self.url,
            headers=self.headers,
            params=self.params,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def options(self):
        """
        发送OPTIONS请求并返回响应

        :return: 响应对象
        """
        response = requests.options(
            url=self.url,
            headers=self.headers,
            params=self.params,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    def patch(self):
        """
        发送PATCH请求并返回响应

        :return: 响应对象
        """
        response = requests.patch(
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            timeout=self.timeout,
            **self.kwargs
        )
        return response

    # __repr__ 返回一个 Python 表示该对象的字符串，通常用于交互式控制台和调试时打印。
    def __repr__(self):
        return '<RequestModule [{}]>'.format(self.method)

    # __str__ 返回一个人类可读的字符串，通常用于打印和日志记录。如果 __str__ 没有被定义，则会返回 __repr__ 的结果。
    def __str__(self):
        return '<RequestModule [{}]>'.format(self.method)
