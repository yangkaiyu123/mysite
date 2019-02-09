import pymysql


def get_list(sql, args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='py01db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# def mongo_modify(sql, args):
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient["mongo01db"]
#     mycol = mydb["test01db"]


def get_one(sql, args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='py01db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def modify(sql, args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='py01db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()


def create(sql, args):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='py01db')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    last_row_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_row_id


class SqlHelper(object):
    def __init__(self):
        # 读取配置文件
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='py01db')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def create(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()
        self.conn.close()
