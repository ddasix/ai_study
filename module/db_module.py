import pymysql

class Database():
    def __init__(self):
        self.db= pymysql.connect(host='localhost',
                                  user='ddasix',
                                  password='123123',
                                  db='ai_study',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args) 

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row

    def insert(self, query, args={}):
        self.cursor.execute(query, args)
        last_insert_id = self.cursor.lastrowid
        return last_insert_id

    def commit(self):
        self.db.commit()