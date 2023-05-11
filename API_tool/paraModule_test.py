import unittest
from API_tool.paraModule import ParaModule

class TestParaModule(unittest.TestCase):
    def setUp(self):
        self.module = ParaModule('config.ini')

    def tearDown(self):
        self.module = None

    def test_parse_docx_table(self):
        table = self.module.build_docx_table({'foo': 'bar', 'baz': 'qux'})
        data = self.module.parse_docx_table(table)
        self.assertEqual(data, {'foo': 'bar', 'baz': 'qux'})

    def test_parse_word(self):
        params, headers, checks = self.module.parse_word('example.docx')
        self.assertEqual(params, {'foo': 'bar'})
        self.assertEqual(headers, {'X-Auth-Token': 'secret'})
        self.assertEqual(checks, {'status_code': 200, 'response_body': {'foo': 'bar'}})

    def test_set_config(self):
        self.module.set_config('example', params={'foo': 'bar'}, headers={'X-Auth-Token': 'secret'})
        config = self.module.reload_config('config.ini')
        params = dict(config['example']['params'])
        headers = dict(config['example']['headers'])
        self.assertEqual(params, {'foo': 'bar'})
        self.assertEqual(headers, {'X-Auth-Token': 'secret'})

if __name__ == '__main__':
    unittest.main()




