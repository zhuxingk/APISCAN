import json
import re
from bs4 import BeautifulSoup


class MarkdowntoSql:
    def __init__(self, md_file, sql_file):
        self.md_file = md_file
        self.sql_file = sql_file
        self.sql_list = []

    import re

    def convert_markdown_to_sql(self, sql_path):
        # 读取 markdown 文件内容
        with open(self.md_file, 'r') as f:
            content = f.read()

        # 使用正则表达式匹配接口信息
        pattern = r'##\s+(?P<name>.+)\n\n- URL:\s+(?P<url>.+)\n- Method:\s+(?P<method>\w+)\n- Request:\s+(?P<request>{.*})\n- Response\(TRUE\):\s+(?P<response_true>{.*})\n- Response\(FALSE\):\s+(?P<response_false>{.*})'

        matches = re.findall(pattern, content, flags=re.DOTALL)

        # 循环遍历匹配结果，生成 SQL 语句并写入输出文件
        with open(sql_path, 'w') as f:
            for match in matches:
                name = match[0]
                url = match[1]
                method = match[2]
                request = match[3]
                response_true = match[4]
                response_false = match[5]

                # 替换特殊字符，避免 SQL 注入
                request = request.replace("'", "''")
                response_true = response_true.replace("'", "''")
                response_false = response_false.replace("'", "''")

                # 生成 SQL 语句并写入输出文件
                sql = f"INSERT INTO `api` (`name`, `url`, `method`, `request`, `response(true)`, `response(false)`) VALUES ('{name}', '{url}', '{method}', '{request}', '{response_true}', '{response_false}');"
                f.write(sql + '\n')

            # f.write(sql + '\n')  # 将SQL语句写入文件中
            # f.close()
            print(sql)
if __name__ == '__main__':
    md_file = './test.md'
    sql_file = './test.sql'


