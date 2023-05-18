from pymongo import MongoClient

# 用于测试接口的类
class APITester:
    # 初始化APITester实例
    def __init__(self, mongodb_uri, db_name):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.api_collection = self.db.APICollection
        self.api_response = self.db.APIResponse
    # 获取所有接口的信息
    def get_response_info(self):
        response_true = self.api_collection.find({}, {"Response(TRUE)": 1})
        response_false = self.api_collection.find({}, {"Response(FALSE)": 1})
        api_response = self.api_response.find({}, {"response": 1})
        return response_true, response_false, api_response
    # 比较接口的响应
    def compare_responses(self):
        response_true, response_false, api_response = self.get_response_info()
        # 遍历所有接口
        for api in response_true:
            errorcode = api["Response(TRUE)"].get("errorcode")
            if errorcode == 0:
                print(f"API {api['_id']} test successful.")
            else:
                errormsg = self.get_errormsg(api_response, api["_id"])
                print(f"API {api['_id']} test failed. Error message: {errormsg}")
        # 遍历所有接口
        for api in response_false:
            errorcode = api["Response(FALSE)"].get("errorcode")
            if errorcode == 0:
                print(f"API {api['_id']} test successful.")
            else:
                errormsg = self.get_errormsg(api_response, api["_id"])
                print(f"API {api['_id']} test failed. Error message: {errormsg}")
    # 获取错误信息
    def get_errormsg(self, api_response, api_id):
        response = api_response.find_one({"_id": api_id}, {"response": 1})
        return response["response"].get("errormsg", "")
# 测试接口
if __name__ == "__main__":
    tester = APITester("mongodb://localhost:27017/", "APIInfo")
    tester.compare_responses()

