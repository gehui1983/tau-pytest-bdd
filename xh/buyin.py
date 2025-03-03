import json
import brotli
import pymysql as mysql


class BuyIn:

    def clean_data(self, crawl_data_id=0):
        no_decode_list = list()
        sql_select = '''SELECT id, response_body from CRAWL_DB.CRAWL_DATA WHERE path = %s and id > %s'''
        sql_insert = '''INSERT INTO CRAWL_DB.BUY_IN (source_id,shop_id, shop_name,exp_score,product_id, title, 
                        detail_url, recommend_reason, price, cos_fee, cos_ratio, cos_type, sales, good_ratio, 
                        kol_num, axis, promotion_id, commodity_id) VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        path = '/pc/selection/common/material_list'
        conn = mysql.connect(host="127.0.0.1", port=3306, user='admin',
                             password='admin', database="CRAWL_DB")
        cur = conn.cursor()
        try:
            cur.execute(sql_select, [path, crawl_data_id])
            res = cur.fetchall()
            for r in res:
                ids, response_body = r
                source_id = ids
                print(source_id)
                try:
                    compressed_data = brotli.decompress(response_body)
                except brotli.error:
                    no_decode_list.append(source_id)
                    continue
                res_str = compressed_data.decode("utf-8")
                list_values = list()
                res_json = json.loads(res_str)
                for dict_res in res_json['data']["promotions"]:
                    print(dict_res)
                    shop_info = dict_res['shop_info']
                    shop_id = shop_info['shop_id']
                    shop_name = shop_info['shop_name']
                    try:
                        exp_score = shop_info['exp_score']
                    except KeyError:
                        exp_score = 0
                    product_id = dict_res['product_id']
                    promotion_id = dict_res['promotion_id']
                    commodity_id = ''
                    try:
                        commodity_id = dict_res['other_info']['data_report']['commodity_id']
                    except KeyError:
                        commodity_id = promotion_id
                    base_info = dict_res['base_info']
                    title = base_info['title']
                    detail_url = base_info['detail_url']
                    recommend_reason = ''
                    try:
                        recommend_reason = dict_res['tag_info']['tags']['recommend_reason']['text']
                    except KeyError:
                        try:
                            recommend_reason = dict_res['other_info']['data_report']['recommend_reason_text']
                        except KeyError:
                            pass
                    price = dict_res['price_info']['price']
                    cos_info = dict_res['cos_info']
                    cos_fee = cos_info['cos_fee']
                    cos_ratio = cos_info['cos_ratio']
                    try:
                        cos_type = cos_info['cos_type']
                    except KeyError:
                        cos_type = -1
                    manage_info = dict_res['manage_info']
                    sales = manage_info['sales']
                    good_ratio = ''
                    try:
                        good_ratio = manage_info['good_ratio']
                    except KeyError:
                        pass
                    kol_num = manage_info['kol_num']
                    try:
                        axis = str(manage_info['axis'])
                    except KeyError:
                        pass
                    list_values.append((source_id, shop_id, shop_name, exp_score, product_id, title, detail_url,
                                        recommend_reason, price, cos_fee, cos_ratio, cos_type, sales, good_ratio,
                                        kol_num, axis, promotion_id, commodity_id))
                    print(list_values)
                cur.executemany(sql_insert, list_values)
                cur.connection.commit()
                # break

        except mysql.MySQLError as e:
            print(e.args)
        finally:
            cur.close()
            conn.close()
            print("执行完毕")
            print(no_decode_list)

    def sql_execute_02(self,host="192.168.3.145", crawl_data_id=11803):
        sql_select = '''SELECT id, response_body from CRAWL_DB.CRAWL_DATA WHERE id = %s'''
        conn = mysql.connect(host="127.0.0.1", port=3306, user='admin',
                             password='admin', database="CRAWL_DB")
        cur = conn.cursor()
        try:
            cur.execute(sql_select, [ crawl_data_id])
            res = cur.fetchall()
            for t in res:
                data_id, response_body = t
                print( data_id)
                # print(response_body)
                try:
                    compressed_data = brotli.decompress(response_body)
                    print(compressed_data)
                except brotli.error:
                    print("解压失败")
                    print(brotli.error.args)
        except mysql.MySQLError as e:
            print(e.args)
        finally:
            cur.close()
            conn.close()
            print("执行完毕")

    def source_to_target(self,crawl_data_id=1):

        sql_insert = '''INSERT INTO CRAWL_DB.CRAWL_DATA(`method`, `host`, `path`, `query`, `cookie`, `request_head`, `request_body`, `response_head`, `response_body` ) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        target_conn = mysql.connect(host="127.0.0.1", port=3306, user='admin',
                             password='admin', database="CRAWL_DB")
        target_cur = target_conn.cursor()

        path0 = '/pc/selection/common/material_list'
        sql_select = '''SELECT `id`,`method`, `host`, `path`, `query`, `cookie`, `request_head`, `request_body`, `response_head`, `response_body` 
                        FROM CRAWL_DB.CRAWL_DATA 
                        WHERE path = %s and id > %s'''
        source_conn = mysql.connect(host="192.168.3.145", port=3306, user='admin',
                             password='admin', database="CRAWL_DB")
        try:
            with source_conn.cursor() as source_cur:
                source_cur.execute(sql_select, [path0, crawl_data_id])
                for row in source_cur:
                    data_id,method, host, path, query, cookie, request_head, request_body, response_head, response_body = row
                    target_cur.execute(sql_insert,[method, host, path, query, cookie, request_head, request_body, response_head, response_body])
                    target_cur.connection.commit()
                    print( data_id)
        except mysql.MySQLError as e:
            print(e.args)
        finally:
            source_conn.close()
            target_cur.close()
            target_conn.close()
            print("执行完毕")


# -- 分组后,查询,记录数量
# select count(*) from (SELECT COUNT(bi.shop_id)as count, bi.shop_id from BUY_IN bi group by bi.shop_id) a;
# 以下是不能解压缩
# [797, 1292, 1297, 1309, 1314, 1315, 1317, 1319, 1323, 1324, 1326, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337,
# 3366]
# [4726, 4768, 4850, 5233, 5317, 5359, 5401, 5826, 5940]
# [7845, 7919, 8105, 9026]
# [10047, 10225, 10299, 10844, 10926, 11414]
# [13166, 13224, 14360]
# [14552, 14699, 14760, 14874, 16809, 16825, 17462]
# [19809, 19868, 20108, 20147, 20456, 20485, 20689, 21746, 22587]

if __name__ == '__main__':
    buy = BuyIn()
    # buy.source_to_target(crawl_data_id=14026)
    buy.clean_data(crawl_data_id=24510)

    # buy.sql_execute_02(crawl_data_id=11802)

# SELECT COUNT(*) from CRAWL_DB.CRAWL_DATA WHERE `path`='/pc/selection/common/material_list' and id > 19739;
# select count(*) from (SELECT COUNT(bi.shop_id)as count, bi.shop_id from BUY_IN bi group by bi.shop_id) a;
# -- 最大店铺数量: 15238
# -- source_id:19739
# -- 1, source_id=3370, 爬取=3103条，增加店铺数量：9411-7407=2004
# -- 2, source_id=6467, 爬取=3204条, 增加店铺数量:10796-9411=1385
# -- 3, source_id=12915 爬取=3240条, 增加店铺数量:12448-10796=1652
# -- 4, source_id=14373 爬取=1458条, 增加店铺数量:13444-12448=996
# -- 5, source_id=17794 爬取=3421条, 增加店铺数量:14618-13444=1174
# -- 6, source_id=19739 爬取=1945条, 增加店铺数量:15238-14618=620
# SELECT * from CRAWL_DATA cd WHERE cd.id = 4726;
#
# select MAX(bi.source_id) from CRAWL_DB.BUY_IN_01 bi;


# 最大店铺数量：8778
# -- source_id:25520
# -- 1, source_id=1, 爬取=9348条，增加店铺数量：5679-0=5679
#       无法执行 [254, 415, 502, 621, 865, 878, 882, 901, 902, 912, 914, 915, 916, 917, 919, 921, 923, 924, 926, 927, 929, 931, 932, 935, 936, 937, 999, 2522, 2585, 2619, 2687, 3688, 4114, 4145, 4822, 7394, 7885, 8011, 8016, 8041]
# --3, source_id=1  爬取=3186条，增加店铺数量：6815-5679=1136
#       无法执行 [10936, 11974, 12544, 12663]
# --4, source_id=13674  爬取=5827条，增加店铺数量：7746-6815=931
#       无法执行 [13688, 13710, 14751, 15449, 16267, 16283, 16910, 17562, 17885, 19079]
#
# --5, source_id=24510  爬取=5013条，增加店铺数量：8590-7746=844
# 无法执行  [19719, 20497, 22350, 23539, 23784]
# --5, source_id=25520  爬取=1010条，增加店铺数量：8778-8590=188
# 无法执行  [25086, 25253, 25275, 25332]
# 192.168.3.145   max(id) = 15036