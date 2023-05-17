import json
import re

import markdown2
from bs4 import BeautifulSoup


class MarkdowntoSql:
    def __init__(self, md_file, sql_file):
        self.md_file = md_file
        self.sql_file = sql_file

    def convert_markdown_to_sql(self, sql_file):
        # 从Markdown文档中读取输入数据
        with open(md_file, 'r') as file:
            input_data = file.read()
            print(input_data)

        #将markdown文档中的数据转换为html格式
        html = markdown2.markdown(input_data)

        # 使用正则表达式提取接口信息
        pattern = r'<h2>\s*API\d+\s*</h2>\s*<ul>\s*<li>URL:\s*(.*?)\s*</li>\s*<li>Method:\s*(.*?)\s*</li>\s*<li>Request:\s*<pre><code>(.*?)</code></pre>\s*</li>\s*<li>Response\(TRUE\):\s*<pre><code>(.*?)</code></pre>\s*</li>\s*<li>Response\(FALSE\):\s*<pre><code>(.*?)</code></pre>\s*</li>\s*</ul>'
        matches = re.findall(pattern, html, re.DOTALL)
        print(matches)  # 打印匹配结果

        # 处理每个接口
        for match in matches:
            url = match[0].strip()
            method = match[1].strip()
            request = match[2].strip()
            response_true = match[3].strip()
            response_false = match[4].strip()

            # 构建插入语句
            insert_statement = f"INSERT INTO `api` (`name`, `url`, `method`, `request`, `response(true)`, `response(false)`) \
        VALUES ('{url}', '{method}', '{request}', '{response_true}', '{response_false}');"
            print(insert_statement)
            # 将生成的语句写入到sql.file文件中
            with open(sql_file, 'a') as file:
                file.write(insert_statement + '\n')


if __name__ == '__main__':
    md_file = './test.md'
    sql_file = './test.sql'

    mts = MarkdowntoSql(md_file, sql_file)
    mts.convert_markdown_to_sql(sql_file)
