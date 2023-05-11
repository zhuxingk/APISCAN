import markdown
from bs4 import BeautifulSoup


class MarkdowntoSql:
    def __init__(self, md_file, sql_file):
        self.md_file = md_file
        self.sql_file = sql_file
        self.sql_list = []

    def parse_markdown(self):
        # 解析markdown文本
        with open(self.md_file, encoding='utf-8') as f:
            md = f.read()
        print(md)

        # 解析markdown表格
        soup = BeautifulSoup(md, 'html.parser')
        tables = soup.find_all('table')

        for table in tables:
            headers = [header.get_text() for header in table.find_all('th')]
            rows = table.find_all('tr')
            for row in rows:
                values = [value.get_text().strip() for value in row.find_all('td')]
                if len(headers) == len(values):
                    # 根据解析到的值生成sql语句
                    self.sql_list.append(self.generate_sql(headers, values))
        print(self.sql_list)

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
            print(sql)

            # 如果存在response(false)，生成一条额外的insert语句
            if response_false:
                sql = f"INSERT INTO interface_info (interface_name, interface_url, request_method, request_header, request_parameter, response) VALUES ('', '{url}', '{method}', '', '{request}', '{response_false}')"
                self.sql_list.append(sql)
                print(sql)

    def write_sql(self, file_path):
        # 将生成的sql语句存储到指定文件中
        with open(file_path, 'w') as f:
            f.write('\n'.join(self.sql_list))
            print('\n'.join(self.sql_list))
        print('SQL file generated successfully')

    def decode_sql(self):
        # 解析markdown文本生成sql语句
        self.parse_markdown()
        if not self.sql_list:
            raise Exception('No SQL generated from the markdown file')
        self.write_sql(self.sql_file)
        print('SQL file generated successfully')


if __name__ == '__main__':
    md_file = './test.md'
    sql_file = './test.sql'
    MarkdowntoSql(md_file, sql_file).decode_sql()
