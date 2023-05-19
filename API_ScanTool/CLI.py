import argparse

from API_ScanTool.MongoDBClient import MongoDBClient
from SendReq import APISender
from Choice import Choice


class CLI:
    def __init__(self, mongodb_url, database_name):
        self.mongodb_client = MongoDBClient(mongodb_url, database_name)
        self.sender = APISender(self.mongodb_client, collection_name='APICollection', response_name='APIResponses')
        self.choice = Choice(mongodb_url, database_name)


    def run(self):
        parser = self.create_parser()
        args = parser.parse_args()

        if args.default:
            self.execute_all_apis()
        elif args.name:
            self.execute_selected_api(args.name)

    def create_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--default', action='store_true', help='Execute all APIs')
        parser.add_argument('-n', '--name', help='API name')
        # args = parser.parse_args()
        return parser

    def run(self):
        parser = self.create_parser()
        args = parser.parse_args()

        if args.default:
            self.execute_all_apis()
        elif args.name:
            self.execute_selected_api(args.name)



    def execute_all_apis(self):
        api_names = self.sender.get_api_names()
        for api_name in api_names:
            result = self.choice.execute_selected_api(api_name)
            self.process_result(api_name, result)

    def execute_selected_api(self, api_name):
        result = self.choice.execute_selected_api(api_name)
        self.process_result(api_name, result)

    def process_result(self, api_name, result):
        if 'error' in result:
            print(f"API '{api_name}' execution failed. Error: {result['error']}")
        else:
            status_code = result['status_code']
            response = result['response']
            print(f"API '{api_name}' executed successfully. Status code: {status_code}")
            print(f"Response: {response}")

        api_info = self.choice.collection.find_one({'name': api_name})
        url = api_info['URL']
        method = api_info['Method']
        request = api_info['Request']
        self.sender.save_response(api_name, url, method, request, status_code, response)


# if __name__ == '__main__':
#     mongodb_url = 'mongodb://localhost:27017/'
#     database_name = 'APIInfo'
#     CLI(mongodb_url, database_name).run()



