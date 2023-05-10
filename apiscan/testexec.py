import unittest
import requests
from requests.exceptions import HTTPError
from config import Config
from apimanage import InterfaceDB


class ApiTestCase(unittest.TestCase):
    def __init__(self, name, url, method, headers=None, params=None, data=None, check_type=None, check_value=None):
        super(ApiTestCase, self).__init__()
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.check_type = check_type
        self.check_value = check_value

    def test_case(self):
        try:
            response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=self.data,
            )
            response.raise_for_status()
            if self.check_type == 'status_code':
                self.assertEqual(response.status_code, self.check_value)
            elif self.check_type == 'content':
                self.assertIn(self.check_value, response.content.decode('utf-8'))
        except HTTPError as e:
            print(e)

class TestSuite:
    def __init__(self, config_file, db_file):
        self.config = Config(config_file)
        self.db = InterfaceDB(db_file)
        self.db.create_table()

    def add_test_case(self, name):
        section = self.config.get(name, 'section')
        options = self.config.get_options(section)
        url = self.config.get(section, 'url')
        method = self.config.get(section, 'method')
        headers = self.config.get(section, 'headers')
        params = self.config.get(section, 'params')
        data = self.config.get(section, 'data')
        check_type = self.config.get(section, 'check_type')
        check_value = self.config.get(section, 'check_value')
        test_case = ApiTestCase(
            name=name,
            url=url,
            method=method,
            headers=headers,
            params=params,
            data=data,
            check_type=check_type,
            check_value=check_value
        )
        return test_case

    def run(self):
        test_suite = unittest.TestSuite()
        sections = self.config.get_sections()
        for section in sections:
            test_case = self.add_test_case(section)
            test_suite.addTest(test_case)
        runner = unittest.TextTestRunner()
        runner.run(test_suite)
