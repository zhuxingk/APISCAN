import unittest
from API_tool.requestModule import RequestModule, select


class RequestModuleTest(unittest.TestCase):

    def test_select(self):
        self.assertEqual(select('GET'), RequestModule.get)
        self.assertEqual(select('POST'), RequestModule.post)
        self.assertEqual(select('PUT'), RequestModule.put)
        self.assertEqual(select('DELETE'), RequestModule.delete)
        self.assertEqual(select('HEAD'), RequestModule.head)
        self.assertEqual(select('OPTIONS'), RequestModule.options)
        self.assertEqual(select('PATCH'), RequestModule.patch)
        self.assertIsNone(select('UNKNOWN_METHOD'))

if __name__ == '__main__':
    unittest.main()
