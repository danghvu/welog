import sqlite3

DBNAME = "tempdb.db"

class DB:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS msg ( \
                             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                             user TEXT, \
                             channel TEXT, \
                             message TEXT, \
                             time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    def __def__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def write(self, user, channel, message):
        self.cursor.execute("INSERT INTO msg ( user, channel, message ) VALUES (?, ?, ?)", (user, channel, message))
        self.conn.commit()

    def read(self, channel=None):
        if channel is None:
            return self.cursor.execute("SELECT time,channel,user,message FROM msg ORDER BY time ASC").fetchall()
        else:
            return self.cursor.execute("SELECT time,user,message FROM msg WHERE channel=? ORDER BY time ASC", ("#"+channel,)).fetchall()

    def listChannel(self):
        return self.cursor.execute("SELECT DISTINCT channel FROM msg").fetchall()

dbClient = DB(DBNAME)

if __name__ == "__main}__":
    data = dbClient.read()
    print data[0]
