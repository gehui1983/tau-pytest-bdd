import json

import pymysql as mysql

def sql_execute_02(host="127.0.0.1"):
    sql_select = '''SELECT id, response_body from CRAWL_DB0.CRAWL_DATA WHERE `path` = %s and `host` = %s'''

    sql_insert = '''INSERT INTO CRAWL_DB0.distrit_code (`code`, `name`, `parent_code`, `level`) VALUES (%s, %s, %s, %s)'''

    sql_count = '''SELECT COUNT(*) as c FROM CRAWL_DB0.distrit_code where `code` = %s and `level` = %s'''
    conn = mysql.connect(host=host, port=3306, user='admin',
                         password='admin', database="CRAWL_DB0")
    cur = conn.cursor()
    try:
        cur.execute(sql_select, ["/api/ListRegion", "www.lddgo.net"])
        res = cur.fetchall()
        for t in res:
            data_id, response_body = t
            body = str(response_body, "utf-8")
            try:
                body_dict = json.loads(body)
                print(body)
                data = body_dict["data"]
                insert_list = list()
                for d in data:
                    parent_id =  d["parentID"] if d["parentID"] is not None else "000000"
                    ids = d["id"]
                    name = d["name"]
                    level = d["level"]
                    cur.execute(sql_count, [ids, level])
                    count :int = cur.fetchone()[0]
                    if count == 0:
                        insert_list.append((ids, name, parent_id, level))

                cur.executemany(sql_insert, insert_list)
                cur.connection.commit()
            except json.decoder.JSONDecodeError:
                pass
    except mysql.MySQLError as e:
        print(e.args)
    finally:
        cur.close()
        conn.close()
        # print("执行完毕")

if __name__ == '__main__':
    sql_execute_02()
