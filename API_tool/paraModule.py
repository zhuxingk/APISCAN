import configparser
import os
import re

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



    def request(self, method, url, params=None, data=None, json=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None, verify=None, stream=None, cert=None):
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

    def para_markdown(self, markdown_file):
        """Parse parameters from a markdown file.

        Args:
            markdown_file (str): Path to markdown file.

        Returns:
            dict: A dictionary of parameters.
        """
        with open(markdown_file, 'r') as f:
            text = f.read()

        html = markdown.markdown(text)
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table')
        if not table:
            raise ValueError('No table found in the markdown file')

        header = table.find_all('th')
        if len(header) != 3:
            raise ValueError('Table header should contain exactly three columns')

        name_col, type_col, desc_col = header
        if name_col.text != 'Name' or type_col.text != 'Type' or desc_col.text != 'Description':
            raise ValueError('Table header columns should be named "Name", "Type", and "Description"')

        params = {}
        rows = table.find_all('tr')[1:]  # skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) != 3:
                raise ValueError('Table rows should contain exactly three columns')

            name, type_, desc = [col.text.strip() for col in cols]
            if not name:
                continue

            # convert type to native Python type
            if type_ == 'int':
                type_ = int
            elif type_ == 'float':
                type_ = float
            elif type_ == 'bool':
                type_ = bool

            params[name] = {
                'type': type_,
                'description': desc,
            }

        return params

    def para_table(self, table_file):
        """
        Parse parameters from a table file.

        Args:
            table_file (str): Path to table file.

        Returns:
            dict: A dictionary of parameters.
        """
        with open(table_file, 'r') as f:
            text = f.read()

        lines = text.strip().split('\n')
        header = lines[0].strip().split('|')
        if len(header) != 3:
            raise ValueError('Table header should contain exactly three columns')

        name_col, type_col, desc_col = header
        if name_col.strip() != 'Name' or type_col.strip() != 'Type' or desc_col.strip() != 'Description':
            raise ValueError('Table header columns should be named "Name", "Type", and "Description"')

        params = {}
        for line in lines[2:]:  # skip header and separator rows
            cols = re.split(r'\s*\|\s*', line.strip())
            if len(cols) != 3:
                raise ValueError('Table rows should contain exactly three columns')

            name, type_, desc = [col.strip() for col in cols]
            if not name:
                continue

            # convert type to native Python type
            if type_ == 'int':
                type_ = int
            elif type_ == 'float':
                type_ = float
            elif type_ == 'bool':
                type_ = bool

            params[name] = {
                'type': type_,
                'description': desc,
            }

        return params

    def parse_word(self, word_file, params_table_index=1, headers_table_index=2, checks_table_index=3):
        """
        解析Word文档，返回接口请求参数、头信息和响应结果检查条件
        将参数表、头信息表和响应检查表的索引从硬编码改为可配置的参数，以便在处理不同的Word文档时可以轻松配置
        params_table_index、headers_table_index和checks_table_index
        参数没有提供，则默认为1、2和3
        """
        document = docx.Document(word_file)
        tables = document.tables
        params_table = tables[params_table_index - 1]
        headers_table = tables[headers_table_index - 1]
        checks_table = tables[checks_table_index - 1]
        params = self.parse_docx_table(params_table)
        headers = self.parse_docx_table(headers_table)
        checks = self.parse_docx_table(checks_table)
        return params, headers, checks

    def parse_docx_table(self, table):
        """
        解析Word表格，返回字典形式的数据
        处理表格中可能存在空行的情况：目前的实现假定表格中每一行都是有效的，
        如果表格中存在空行，则会引发IndexError异常。为了处理这种情况，
        可以在循环前加入判断表格是否为空，以及在循环中判断行是否为空，以跳过空行的处理。

        处理表格中可能存在重复键的情况：
        目前的实现将表格中每一行的第一列作为键，第二列作为值，如果表格中存在重复键，
        则会覆盖前面的键值。为了处理这种情况，可以将键作为字典的键，将所有值作为一个列表存储为字典的值。
        这样，每个键对应的值就是一个列表，可以存储所有与该键对应的值。
        """
        data = {}
        if not table.rows:
            return data
        for row in table.rows:
            if not row.cells:
                continue
            key = row.cells[0].text.strip()
            value = row.cells[1].text.strip()
            if key in data:
                if isinstance(data[key], list):
                    data[key].append(value)
                else:
                    data[key] = [data[key], value]
            else:
                data[key] = value
        return data


    def set_config(self, section, params=None, headers=None, checks=None):
        """
        设置接口请求的参数和头信息，以及响应结果的检查条件
        参数的校验：set_config函数的参数section应该是一个非空字符串，
        params、headers和checks应该是字典。在函数中应该加入参数的类型和值的校验，以防止传入不正确的参数。
        """
        if not isinstance(section, str) or not section:
            raise ValueError('section should be a non-empty string')
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if checks is None:
            checks = {}
        if not isinstance(params, dict):
            raise ValueError('params should be a dict')
        if not isinstance(headers, dict):
            raise ValueError('headers should be a dict')
        if not isinstance(checks, dict):
            raise ValueError('checks should be a dict')
        self.config[section] = {
            'params': params,
            'headers': headers,
            'checks': checks
        }
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def reload_config(self, config_file):
        """
        加载配置文件，返回ConfigParser对象
        文件的写入：在将配置写入文件之前，应该先检查文件的路径是否存在。如果路径不存在，应该先创建路径再进行写入操作。
        """
        if not isinstance(config_file, str) or not os.path.isfile(config_file):
            raise ValueError('config_file should be a valid file path')
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

