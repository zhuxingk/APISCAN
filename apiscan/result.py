import json


class ResultReporter:
    def __init__(self, test_results):
        self.test_results = test_results

    def to_json(self):
        results = []
        for test_result in self.test_results:
            results.append({
                'name': test_result.name,
                'result': test_result.result,
                'details': test_result.details
            })
        return json.dumps(results, ensure_ascii=False, indent=4)

    def to_console(self):
        for test_result in self.test_results:
            print(f"Test case '{test_result.name}' result: {test_result.result}")
            print(f"Details: {test_result.details}")
