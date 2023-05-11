import unittest
from requestModule import RequestModule


class TestRequestModule(unittest.TestCase):

    # 这个函数用来初始化测试环境
    def setUp(self):
        self.url = 'https://httpbin.org/get'
        self.headers = {'User-Agent': 'APIscan'}
        self.params = {'key1': 'value1', 'key2': 'value2'}
        self.data = {'foo': 'bar'}

    # 这个函数用来清理测试环境
    def test_init(self):
        request = RequestModule(self.url, method='POST', headers=self.headers, params=self.params, data=self.data,
                                timeout=30)
        self.assertEqual(request.url, self.url)
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.headers, self.headers)
        self.assertEqual(request.params, self.params)
        self.assertEqual(request.data, self.data)
        self.assertEqual(request.timeout, 30)

    def test_repr(self):
        request = RequestModule(self.url)
        self.assertEqual(str(request), '<RequestModule [GET]>')

    def test_str(self):
        request = RequestModule(self.url)
        self.assertEqual(repr(request), '<RequestModule [GET]>')


if __name__ == '__main__':
    # request = RequestModule('http://example.com', timeout=30)
    # print(request)
    unittest.main()
