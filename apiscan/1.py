import requests

class RequestModule:
    def __init__(self, headers=None, timeout=10):
        self.headers = headers
        self.timeout = timeout

    def send_request(self, method, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        response = requests.request(method, url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)
        return response

    def get(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.get(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)

    def post(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.post(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)

    def put(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.put(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)

    def delete(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.delete(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)

    def head(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.head(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)

    def options(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.options(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)

    def patch(self, url, headers=None, params=None, data=None, json=None):
        headers = headers or self.headers
        return requests.patch(url, headers=headers, params=params, data=data, json=json, timeout=self.timeout)
