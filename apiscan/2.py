import configparser
import API_tool.requestModule as RequestModule
import docx
import markdown
import requests
from bs4 import BeautifulSoup


class ParaModule:
    def __init__(self, config_file):
        self.config = self.reload_config(config_file)

    def load_config(self, config_file, yaml=None):
        """
        读取配置文件，返回配置信息
        load_config函数根据配置文件的后缀名来确定文件格式，
        目前支持ini和yaml两种格式。如果配置文件格式不支持，则抛出ValueError异常。
        如果成功加载配置文件，则返回解析后的配置信息。
        """
        try:
            with open(config_file, 'r') as f:
                if config_file.endswith('.yaml'):
                    config = yaml.safe_load(f)
                else:
                    config = dict()
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            config[key.strip()] = value.strip()
        except Exception as e:
            raise ValueError(f'Failed to load configuration file {config_file}: {str(e)}')
        return config



    def request(self, method, url, params=None, data=None, json=None, headers=None,
                cookies=None, files=None,auth=None, timeout=None, allow_redirects=True,
                proxies=None, verify=None, stream=None, cert=None):
        """Send HTTP request.

        Args:
            method (str): HTTP method, e.g. 'GET', 'POST', 'PUT', 'DELETE'.
            url (str): URL of the request.
            params (dict, optional): Query parameters to include in the request.
            data (dict, optional): Data to include in the request body.
            json (dict, optional): JSON data to include in the request body.
            headers (dict, optional): Headers to include in the request.
            cookies (dict, optional): Cookies to include in the request.
            files (dict, optional): Files to include in the request.
            auth (tuple, optional): Authentication credentials.
            timeout (float, optional): Timeout for the request in seconds.
            allow_redirects (bool, optional): Whether to follow redirects.
            proxies (dict, optional): Proxies to use for the request.
            verify (bool, optional): Whether to verify SSL certificates.
            stream (bool, optional): Whether to stream the response.
            cert (str, optional): Path to client certificate file.

        Returns:
            requests.Response: response object.
        """
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise ValueError(f'Invalid HTTP method: {method}')

        response = requests.request(method=method, url=url, params=params, data=data, json=json, headers=headers,
                                    cookies=cookies, files=files, auth=auth, timeout=timeout,
                                    allow_redirects=allow_redirects, proxies=proxies, verify=verify, stream=stream,
                                    cert=cert)
        return response

    # def request(self, method, url, headers=None, params=None, data=None, json=None):
    #     """
    #     发送接口请求
    #     """
    #     if headers is None:
    #         headers = self.config['DEFAULT']['headers']
    #     else:
    #         headers = self.merge_config(headers, self.config['DEFAULT']['headers'])
    #     if params is None:
    #         params = {}
    #     if data is None:
    #         data = {}
    #     if json is None:
    #         json = {}
    #     response = requests.request(method, url, headers=headers, params=params, data=data, json=json)
    #     return response

    def parse_markdown(self, markdown_file):
        """
        解析Markdown文件，返回接口请求参数、头信息和响应结果检查条件
        """
        with open(markdown_file, 'r') as f:
            content = f.read()
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        param_table = soup.find('table', {'class': 'params'})
        header_table = soup.find('table', {'class': 'headers'})
        check_table = soup.find('table', {'class': 'checks'})
        params = self.parse_table(param_table)
        headers = self.parse_table(header_table)
        checks = self.parse_table(check_table)
        return params, headers, checks

    def parse_table(self, table):
        """
        解析HTML表格，返回字典形式的数据
        """
        data = {}
        if table is not None:
            rows = table.findAll('tr')
            for row in rows:
                cells = row.findAll('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    data[key] = value
        return data

    def parse_word(self, word_file):
        """
        解析Word文档，返回接口请求参数、头信息和响应结果检查条件
        """
        document = docx.Document(word_file)
        tables = document.tables
        params_table = tables[0]
        headers_table = tables[1]
        checks_table = tables[2]
        params = self.parse_docx_table(params_table)
        headers = self.parse_docx_table(headers_table)
        checks = self.parse_docx_table(checks_table)
        return params, headers, checks

    def parse_docx_table(self, table):
        """
        解析Word表格，返回字典形式的数据
        """
        data = {}
        for row in table.rows:
            key = row.cells[0].text.strip()
            value = row.cells[1].text.strip()
            data[key] = value
        return data

    def set_config(self, section, params=None, headers=None, checks=None):
        """
        设置接口请求的参数和头信息，以及响应结果的检查条件
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if checks is None:
            checks = {}
        self.config[section] = {
            'params': params,
            'headers': headers,
            'checks': checks
        }
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def reload_config(self, config_file):
        """
        加载配置文件，返回ConfigParser对象
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        return config
