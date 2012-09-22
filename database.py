import sqlite3

DBNAME = "tempdb.db"

class DB:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS msg ( \
                             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                             user TEXT, \
                             command TEXT, \
                             target TEXT, \
                             message TEXT, \
                             time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    def __def__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def write(self):
        #TODO
        pass

    def read(self):
        #TODO
        pass

dbClient = DB(DBNAME)
