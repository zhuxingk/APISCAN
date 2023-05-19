import argparse
from MongoDBClient import MongoDBClient
from SendReq import APISender
from Choice import Choice
from logging_manager import LogManager

class CLI:
    def __init__(self, mongodb_url, database_name):
        self.mongodb_client = MongoDBClient(mongodb_url, database_name)
        self.sender = APISender(self.mongodb_client, collection_name='APICollection', response_name='APIResponses')
        self.choice = Choice(mongodb_url, database_name)

        self.log_manager = LogManager('api_scan_tool.log')

    def run(self):
        self.log_manager.log_debug('API Scan Tool started.')
        while True:
            self.print_menu()
            choice = input('Enter your choice: ')

            if choice == '1':
                self.execute_all_apis()
            elif choice == '2':
                self.execute_selected_api()
            elif choice.lower() == 'q':
                break
            else:
                print('Invalid choice. Please try again.')

        self.log_manager.log_debug('API Scan Tool finished.')

    def print_menu(self):
        print('--- API Scan Tool Menu ---')
        print('1. Default Test')
        print('2. Test by API Name')
        print('q. Quit')

    def execute_all_apis(self):
        api_names = self.sender.get_api_names()
        for api_name in api_names:
            result = self.choice.execute_selected_api(api_name)
            self.process_result(api_name, result)

    def execute_selected_api(self):
        while True:
            api_names = self.sender.get_api_names()
            print('Available API Names:')
            for i, api_name in enumerate(api_names, 1):
                print(f'{i}. {api_name}')

            choice = input('Enter the number corresponding to the API you want to test: ')
            if choice.isdigit() and 1 <= int(choice) <= len(api_names):
                api_name = api_names[int(choice) - 1]
                result = self.choice.execute_selected_api(api_name)
                self.process_result(api_name, result)
            elif choice.lower() == 'b':
                return
            elif choice.lower() == 'q':
                quit()
            else:
                print('Invalid choice. Please try again.')

            while True:
                next_action = input("Choose the next action: (C)continue, (B)back, (Q)quit: ")
                if next_action.lower() == 'c':
                    break
                elif next_action.lower() == 'b':
                    break
                elif next_action.lower() == 'q':
                    quit()
                else:
                    print('Invalid choice. Please try again.')

    def process_result(self, api_name, result):
        try:
            if 'error' in result:
                error_message = f"API '{api_name}' execution failed. Error: {result['error']}"
                self.log_manager.log_error(error_message)
            else:
                status_code = result['status_code']
                response = result['response']
                success_message = f"API '{api_name}' executed successfully. Status code: {status_code}"
                self.log_manager.log_info(success_message)
                self.log_manager.log_debug(f"Response: {response}")

            api_info = self.choice.collection.find_one({'name': api_name})
            if api_info:
                url = api_info['URL']
                method = api_info['Method']
                request = api_info['Request']
                self.sender.save_response(api_name, url, method, request, status_code, response)
            else:
                print(f"API '{api_name}' not found.")
        except Exception as e:
            error_message = f"An error occurred while processing the result of API '{api_name}'. Error: {str(e)}"
            self.log_manager.log_error(error_message)


if __name__ == '__main__':
    mongodb_url = 'mongodb://localhost:27017/'
    database_name = 'APIInfo'
    CLI(mongodb_url, database_name).run()
