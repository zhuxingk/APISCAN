import sqlite3


class InterfaceDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS interface (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            method TEXT NOT NULL,
            headers TEXT,
            params TEXT,
            data TEXT,
            check_type TEXT,
            check_value TEXT
        )
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def insert(self, name, url, method, headers=None, params=None, data=None, check_type=None, check_value=None):
        insert_sql = '''
        INSERT INTO interface (name, url, method, headers, params, data, check_type, check_value)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(insert_sql, (name, url, method, headers, params, data, check_type, check_value))
        self.conn.commit()

    def update(self, id, name, url, method, headers=None, params=None, data=None, check_type=None, check_value=None):
        update_sql = '''
        UPDATE interface
        SET name=?, url=?, method=?, headers=?, params=?, data=?, check_type=?, check_value=?
        WHERE id=?
        '''
        self.cursor.execute(update_sql, (name, url, method, headers, params, data, check_type, check_value, id))
        self.conn.commit()

    def delete(self, id):
        delete_sql = '''
        DELETE FROM interface WHERE id=?
        '''
        self.cursor.execute(delete_sql, (id,))
        self.conn.commit()

    def query_all(self):
        query_sql = '''
        SELECT * FROM interface
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()

    def query_by_id(self, id):
        query_sql = '''
        SELECT * FROM interface WHERE id=?
        '''
        self.cursor.execute(query_sql, (id,))
        return self.cursor.fetchone()
