import markdown
import re
import os


# # 用于实现将接口文件中的接口信息转换为SQL语句，以便于将接口信息存储到数据库中
# class ApiConverter:
#     """
#     将 Markdown 文件转换为 SQL 语句
#     """
#
#     def __init__(self, md_file, sql_file):
#         self.md_file = md_file
#         self.sql_file = sql_file
#
#     def run(self):
#         # 读取 Markdown 文件内容
#         with open(self.md_file, 'r', encoding='utf-8') as f:
#             md_content = f.read()
#
#         # 将 Markdown 转换为 HTML
#         html_content = markdown.markdown(md_content)
#
#         # 解析 HTML，获取接口信息
#         pattern = r'<h2>(.*?)</h2>.*?URL：(.*?)；.*?method：(.*?)；.*?request：(.*?)(?=response).*?response（TRUE）：(.*?)(?=response（FALSE）|$)'
#         interfaces = re.findall(pattern, html_content, re.DOTALL)
#
#         # 生成 SQL 语句并保存到文件
#         with open(self.sql_file, 'w', encoding='utf-8') as f:
#             for interface in interfaces:
#                 sql = self.generate_sql(*interface)
#                 f.write(sql)
#                 f.write('\n')



# class MarkdownToSql:
#     def __init__(self, markdown_file):
#         self.markdown_file = markdown_file
#         self.sql_file = os.path.splitext(self.markdown_file)[0] + '.sql'
#
#     def generate_sql(self):
#         # 读取markdown文件内容
#         with open(self.markdown_file, 'r', encoding='utf-8') as f:
#             markdown_content = f.read()
#
#         # 利用正则表达式匹配接口信息
#         pattern = r'name:(.*)URL:(.*)method:(.*)request:(.*)response\(TRUE\):(.*)response\(FALSE\):(.*)'
#         matches = re.findall(pattern, markdown_content, re.S)
#
#         # 生成SQL语句
#         sql_statements = []
#         for match in matches:
#             interface_name = match[0].strip()
#             interface_url = match[1].strip()
#             request_method = match[2].strip()
#             request_parameter = match[3].strip()
#             response_true = match[4].strip()
#             response_false = match[5].strip()
#
#             # 构建SQL语句
#             sql_statement = f"INSERT INTO interface_info (interface_name, interface_url, request_method, request_parameter, response_true, response_false) VALUES ('{interface_name}', '{interface_url}', '{request_method}', '{request_parameter}', '{response_true}', '{response_false}');"
#
#             sql_statements.append(sql_statement)
#
#         # 将SQL语句写入文件
#         with open(self.sql_file, 'w', encoding='utf-8') as f:
#             f.write('\n'.join(sql_statements))
#
#         return sql_statements
#
# if __name__ == '__main__':
#     markdown_file = r'test.md'
#     markdown_to_sql = MarkdownToSql(markdown_file)
#     markdown_to_sql.generate_sql()
import re


# class MarkdownToSql:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.sql_list = []
#
#     def generate_sql(self):
#         with open(self.file_path, encoding='utf-8') as f:
#             content = f.read()
#
#         api_list = re.findall(
#             r'## (.*?)\n- URL: (.*?)\n- Method: (.*?)\n- Request:\n```\n(.*?)```.*?Response\(TRUE\):\n```\n(.*?)```.*?Response\(FALSE\):\n```\n(.*?)```',
#             content, re.S)
#
#         for api in api_list:
#             name = api[0].strip()
#             url = api[1].strip()
#             method = api[2].strip()
#             request = api[3].strip().replace('\n', '')
#             true_response = api[4].strip().replace('\n', '')
#             false_response = api[5].strip().replace('\n', '')
#
#             sql = f"INSERT INTO interface_info (interface_name, interface_url, request_method, request_header, request_parameter, response) VALUES ('{name}', '{url}', '{method}', '', '{request}', '{true_response}');"
#             self.sql_list.append(sql)
#
#             sql = f"INSERT INTO interface_info (interface_name, interface_url, request_method, request_header, request_parameter, response) VALUES ('{name}', '{url}', '{method}', '', '{request}', '{false_response}');"
#             self.sql_list.append(sql)
#
#         if self.sql_list:
#             with open('api.sql', 'w', encoding='utf-8') as f:
#                 f.write('\n'.join(self.sql_list))
#         else:
#             raise Exception('No SQL generated from the markdown file')
import os


class MarkdownToSql:
    def __init__(self, markdown_file):
        self.markdown_file = markdown_file
        self.sql_file = 'api.sql'
        self.sql_list = []

    def parse_markdown(self):
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('##'):
                    sql = "INSERT INTO interface_info (interface_name, interface_url, request_method, request_header, request_parameter, response) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                        lines[i+1].strip(),
                        lines[i+3].split(': ')[1].strip(),
                        lines[i+2].split(': ')[1].strip(),
                        '{}',
                        lines[i+4].strip(),
                        lines[i+6].strip()
                    )
                    self.sql_list.append(sql)
                i += 1

    def generate_sql(self):
        self.parse_markdown()
        if len(self.sql_list) > 0:
            with open(self.sql_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.sql_list))
            print(f'SQL generated and saved in {os.path.abspath(self.sql_file)}')
        else:
            raise Exception('No SQL generated from the markdown file')


if __name__ == '__main__':
    markdown_file = r'D:\pythonProject\APIscan\API_tool\test.md'
    markdown_to_sql = MarkdownToSql(markdown_file)
    markdown_to_sql.generate_sql()
    print(f'Successfully generated {len(markdown_to_sql.sql_list)} SQL statements from {markdown_file}')


import markdown
from bs4 import BeautifulSoup


class MarkdownToSql:
    def __init__(self, markdown_path):
        self.markdown_path = markdown_path
        self.sql_file = 'api.sql'
        self.sql_list = []

    def parse_markdown(self):
        # 解析markdown文本
        with open(self.markdown_path, encoding='utf-8') as f:
            md_text = f.read()

        # 解析markdown表格
        soup = BeautifulSoup(md_text, 'html.parser')
        tables = soup.find_all('table')

        for table in tables:
            headers = [header.get_text() for header in table.find_all('th')]
            rows = table.find_all('tr')
            for row in rows:
                values = [value.get_text().strip() for value in row.find_all('td')]
                if len(headers) == len(values):
                    # 根据解析到的值生成sql语句
                    self.sql_list.append(self.generate_sql(headers, values))

    def generate_sql(self, headers, values):
        # 根据header和value生成sql语句
        if headers[0] == 'URL' and headers[1] == 'Method' and headers[2] == 'Request' and headers[
            3] == 'Response(TRUE)' and headers[4] == 'Response(FALSE)':
            url = values[0]
            method = values[1]
            request = values[2]
            response_true = values[3]
            response_false = values[4]

            # 生成insert语句
            sql = f"INSERT INTO interface_info (interface_name, interface_url, request_method, request_header, request_parameter, response) VALUES ('', '{url}', '{method}', '', '{request}', '{response_true}')"
            self.sql_list.append(sql)

            # 如果存在response(false)，生成一条额外的insert语句
            if response_false:
                sql = f"INSERT INTO interface_info (interface_name, interface_url, request_method, request_header, request_parameter, response) VALUES ('', '{url}', '{method}', '', '{request}', '{response_false}')"
                self.sql_list.append(sql)

    def save_to_file(self, file_path):
        # 将生成的sql语句存储到指定文件中
        with open(file_path, 'w') as f:
            f.write('\n'.join(self.sql_list))

    def generate_sql_from_markdown(self):
        # 解析markdown文本生成sql语句
        self.parse_markdown()
        if not self.sql_list:
            raise Exception('No SQL generated from the markdown file')
        self.save_to_file(self.sql_file)


if __name__ == '__main__':
    markdown_file = r'D:\pythonProject\APIscan\API_tool\test.md'
    markdown_to_sql = MarkdownToSql(markdown_file)
    markdown_to_sql.generate_sql_from_markdown()
