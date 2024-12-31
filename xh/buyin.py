import brotli
import pymysql as mysql


class BuyIn:
    def __init__(self):

        self.db = mysql.connect(host="127.0.0.1", port=3306, user='admin',
                                password='admin', database="CRAWL_DB")
        self.cur = self.db.cursor()

    def sql_execute(self):
        try:
            self.cur.execute('''SELECT id, response_body from CRAWL_DATA 
                                    WHERE id=401''')
            ids, response_body = self.cur.fetchone()
            print(f'id={response_body}')
            compressed_data = brotli.decompress(response_body)

            print(compressed_data.decode("utf-8"))

        except mysql.MySQLError as e:
            print(e.args)
        finally:
            self.cur.close()
            self.db.close()
            print("初始化完毕")


if __name__ == '__main__':
    buy = BuyIn()
    buy.sql_execute()