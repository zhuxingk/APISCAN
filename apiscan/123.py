import re

# 读取 md 文件内容
with open('./test.md', 'r') as f:
    content = f.read()

# 使用正则表达式匹配接口信息
pattern = r'##\s+(?P<name>.+)\n\n- URL:\s+(?P<url>.+)\n- Method:\s+(?P<method>\w+)\n- Request:\s+(?P<request>{.*})\n- Response\(TRUE\):\s+(?P<response_true>{.*})\n- Response\(FALSE\):\s+(?P<response_false>{.*})'

matches = re.findall(pattern, content, flags=re.DOTALL)

# 循环遍历匹配结果，生成 SQL 语句
for match in matches:
    name = match[0].encode('GBK').decode()
    url = match[1]
    method = match[2]
    request = match[3]
    response_true = match[4]
    response_false = match[5]

    # 替换特殊字符，避免 SQL 注入
    request = request.replace("'", "''")
    response_true = response_true.replace("'", "''")
    response_false = response_false.replace("'", "''")

    # 生成 SQL 语句
    sql = f"INSERT INTO `api` (`name`, `url`, `method`, `request`, `response(true)`, `response(false)`) VALUES ('{name}', '{url}', '{method}', '{request}', '{response_true}', '{response_false}');"

    print(sql)




# import json
# import re
# from bs4 import BeautifulSoup
#
#
# class MarkdowntoSql:
#     def __init__(self, md_file, sql_file):
#         self.md_file = md_file
#         self.sql_file = sql_file
#         self.sql_list = []
#
#     def parse_markdown(self):
#         with open(self.md_file, encoding='utf-8') as f:
#             md = f.read()
#
#         # 解析markdown表格
#         soup = BeautifulSoup(md, 'html.parser')
#         tables = soup.find_all('table')
#
#         for table in tables:
#             headers = [header.get_text() for header in table.find_all('th')]
#             rows = table.find_all('tr')
#             for row in rows:
#                 values = [value.get_text().strip() for value in row.find_all('td')]
#                 if len(headers) == len(values):
#                     # 根据解析到的值生成sql语句
#                     self.sql_list.append(self.generate_sql(headers, values))
#
#         # 解析markdown标题和内容
#         sections = re.findall('##\s(.*?)\n([\s\S]*?)(?=##\s|$)', md)
#
#         for title, content in sections:
#             url = ''
#             method = ''
#             request = ''
#             response_true = ''
#             response_false = ''
#
#             # 解析每个section的内容
#             lines = content.split('\n')
#             for line in lines:
#                 if line.startswith('- URL:'):
#                     url = line.replace('- URL:', '').strip()
#                 elif line.startswith('- Method:'):
#                     method = line.replace('- Method:', '').strip()
#                 elif line.startswith('- Request:'):
#                     request_lines = []
#                     index = lines.index(line) + 1
#                     while index < len(lines) and not lines[index].startswith('- Response'):
#                         request_lines.append(lines[index])
#                         index += 1
#                     request = self.parse_json(request_lines, 'Request')
#                 elif line.startswith('- Response(TRUE):'):
#                     response_true_lines = []
#                     index = lines.index(line) + 1
#                     while index < len(lines) and not lines[index].startswith('- Response'):
#                         response_true_lines.append(lines[index])
#                         index += 1
#                     response_true = self.parse_json(response_true_lines, 'Response(TRUE)')
#                 elif line.startswith('- Response(FALSE):'):
#                     response_false_lines = []
#                     index = lines.index(line) + 1
#                     while index < len(lines) and not lines[index].startswith('- Response'):
#                         response_false_lines.append(lines[index])
#                         index += 1
#                     response_false = self.parse_json(response_false_lines, 'Response(FALSE)')
#
#             # 根据解析到的值生成sql语句
#             self.sql_list.append(self.generate_sql(title, url, method, request, response_true, response_false))
#
#         print(self.sql_list)
#
#     def generate_sql(self, *args):
#         sql = "INSERT INTO `api` ("
#         for arg in args:
#             if type(arg) == str:
#                 sql += "`title`, "
#             elif type(arg) == list:
#                 for item in arg:
#                     sql += f"`{item}`, "
#             else:
#                 sql += "`url`, `method`, `request`, `response_true`, `response_false`, "
#                 break
#         sql = sql[:-2] + ") VALUES ("
#         for arg in args:
#             if type(arg) == str:
#                 sql += f"'{arg}', "
#             elif type(arg) == list:
#                 sql += f"'{','.join(arg)}', "
#             else:
#                 sql += f"'{arg}', "
#         sql = sql[:-2] + ");\n"
#         return sql
#
#     def parse_json(self, lines, key):
#         """
#         解析JSON字符串
#         """
#         json_str = ''
#         start = False
#         for line in lines:
#             if line.startswith(f'- {key}:'):
#                 start = True
#             elif start and line.startswith('-'):
#                 break
#             elif start:
#                 json_str += line.strip() + '\n'
#
#         # 处理json字符串
#         try:
#             json_obj = json.loads(json_str)
#             return json.dumps(json_obj, ensure_ascii=False)
#         except:
#             return ''
#
#     def decode_sql(self):
#         self.parse_markdown()
#
#         if not self.sql_list:
#             raise Exception('No SQL generated from the markdown file')
#
#         with open(self.sql_file, 'w', encoding='utf-8') as f:
#
#             for sql in self.sql_list:
#                 f.write(sql)
# if __name__ == '__main__':
#     md_file = './test.md'
#     sql_file = './test.sql'
#     MarkdowntoSql(md_file, sql_file).decode_sql()