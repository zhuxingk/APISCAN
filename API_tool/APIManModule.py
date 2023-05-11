import sqlite3


class APIManModule:
    def __init__(self):
        """
        初始化数据库连接
        """
        self.conn = sqlite3.connect('interface.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        创建表
        """
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS interface_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interface_name TEXT NOT NULL,
            interface_url TEXT NOT NULL,
            request_method TEXT NOT NULL,
            request_header TEXT,
            request_parameter TEXT,
            response TEXT
        )
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_interface(self, name, url, method, header=None, parameter=None, response=None):
        """
        添加接口信息到数据库
        :param name: 接口名称
        :param url: 接口url
        :param method: 请求方法
        :param header: 请求头
        :param parameter: 请求参数
        :param response: 返回结果
        """
        add_interface_sql = '''
        INSERT INTO interface_info (
            interface_name, interface_url, request_method, request_header, request_parameter, response
        )
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(add_interface_sql, (name, url, method, header, parameter, response))
        self.conn.commit()

    def delete_interface(self, name):
        """
        根据接口名称删除接口信息
        :param name: 接口名称
        """
        delete_interface_sql = '''
        DELETE FROM interface_info WHERE interface_name = ?
        '''
        self.cursor.execute(delete_interface_sql, (name,))
        self.conn.commit()

    def update_interface(self, name, url=None, method=None, header=None, parameter=None, response=None):
        """
        更新接口信息
        :param name: 接口名称
        :param url: 接口url
        :param method: 请求方法
        :param header: 请求头
        :param parameter: 请求参数
        :param response: 返回结果
        """
        update_interface_sql = '''
        UPDATE interface_info 
        SET interface_url = COALESCE(?, interface_url), 
        request_method = COALESCE(?, request_method), 
        request_header = COALESCE(?, request_header), 
        request_parameter = COALESCE(?, request_parameter),
        response = COALESCE(?, response)
        WHERE interface_name = ?
        '''
        self.cursor.execute(update_interface_sql, (url, method, header, parameter, response, name))
        self.conn.commit()

    def query_interface(self, name=None):
        """
        查询接口信息
        :param name: 接口名称
        :return: 接口信息列表
        """
        if name:
            query_interface_sql = '''
            SELECT * FROM interface_info WHERE interface_name = ?
            '''
            self.cursor.execute(query_interface_sql, (name,))
        else:
            query_interface_sql = '''
            SELECT * FROM interface_info
            '''
            self.cursor.execute(query_interface_sql)
        return self.cursor.fetchall()

    def close(self):
        """
        关闭数据库连接
        """
        self.conn.close()


