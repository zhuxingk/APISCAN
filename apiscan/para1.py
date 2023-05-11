import configparser
import yaml
import markdown
import docx

class APITool:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """
        读取配置文件，返回配置信息
        """
        ext = config_file.split('.')[-1]
        if ext == 'ini':
            config = configparser.ConfigParser()
            config.read(config_file)
        elif ext == 'yaml':
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config file format: {ext}")
        return config

    def get_request_params(self, api_name):
        """
        获取接口请求参数和头信息
        """
        params = {}
        if api_name in self.config:
            for key, value in self.config[api_name].items():
                if key.startswith('header_'):
                    params['headers'] = {key.replace('header_', ''): value}
                else:
                    params[key] = value
        return params

    def get_response_check(self, api_name):
        """
        获取响应结果的检查条件
        """
        check = {}
        if api_name in self.config:
            for key, value in self.config[api_name].items():
                if key.startswith('check_'):
                    check[key.replace('check_', '')] = value.lower() == 'true'
        return check

    def load_params_from_md(self, md_file):
        """
        从Markdown文件中读取接口请求参数和头信息
        """
        with open(md_file, 'r') as f:
            md_content = f.read()
        html = markdown.markdown(md_content)
        # 解析html，提取参数和头信息
        # ...
        # 将提取到的参数和头信息加入self.config

    def load_params_from_word(self, docx_file):
        """
        从Word文档中读取接口请求参数和头信息
        """
        doc = docx.Document(docx_file)
        # 解析文档，提取参数和头信息
        # ...
        # 将提取到的参数和头信息加入self.config

    def save_config(self, config_file):
        """
        保存配置信息到文件
        """
        ext = config_file.split('.')[-1]
        if ext == 'ini':
            with open(config_file, 'w') as f:
                self.config.write(f)
        elif ext == 'yaml':
            with open(config_file, 'w') as f:
                yaml.dump(self.config, f)
        else:
            raise ValueError(f"Unsupported config file format: {ext}")

    def manual_config(self, api_name):
        """
        手动配置接口请求参数和头信息
        """
        # 创建界面或表单，让用户输入参数和头信息
        # ...
        # 将用户输入的参数和头信息加入self.config

    def send_request(self, api_name):
        """
        发送请求，并检查响应结果
        """
        # 获取请求参数和头信息
        params = self.get_request_params(api_name)
        # 发送请求
        # ...
        # 获取响应结果
        response = {'status': 'success', 'data': {'result': True}}
        # 检查响应结果是否符合预期
        check = self.get_response_check(api_name)
        for key, value in check.items():
            if response['data'][key] != value:
                response['status'] = 'failed'
                break
        return response

