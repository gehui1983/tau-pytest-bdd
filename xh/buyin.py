import json
import brotli
import pymysql as mysql


class BuyIn:
    def __init__(self):

        self.db = mysql.connect(host="127.0.0.1", port=3306, user='admin',
                                password='admin', database="CRAWL_DB")
        self.cur = self.db.cursor()

    def sql_execute_01(self, crawl_data_id=0):
        no_decode_list = list()
        sql_select = '''SELECT id, response_body from CRAWL_DB.CRAWL_DATA WHERE path = %s and id > %s'''
        sql_insert = '''INSERT INTO CRAWL_DB.BUY_IN_01 (source_id,shop_id, shop_name,exp_score,product_id, title, 
                        detail_url, recommend_reason, price, cos_fee, cos_ratio, cos_type, sales, good_ratio, 
                        kol_num, axis, promotion_id, commodity_id) VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        path = '/pc/selection/common/material_list'
        try:
            self.cur.execute(sql_select, [path, crawl_data_id])
            res = self.cur.fetchall()
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
                self.cur.executemany(sql_insert, list_values)
                self.cur.connection.commit()
                # break

        except mysql.MySQLError as e:
            print(e.args)
        finally:
            self.cur.close()
            self.db.close()
            print("执行完毕")
            print(no_decode_list)

    def sql_execute_02(self, path='/pc/selection/common/material_list', crawl_data_id=6477):
        sql_select = '''SELECT id, response_body from CRAWL_DB.CRAWL_DATA WHERE path = %s and id = %s'''
        try:
            self.cur.execute(sql_select, [path, crawl_data_id])
            data_id, response_body = self.cur.fetchone()
            print(response_body)
            try:
                compressed_data = brotli.decompress(response_body)
                print(compressed_data)
            except brotli.error:
                print("解压失败")
                print(brotli.error)
        except mysql.MySQLError as e:
            print(e.args)
        finally:
            self.cur.close()
            self.db.close()
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
    buy.sql_execute_01(crawl_data_id=22987)

# SELECT COUNT(*) from CRAWL_DB.CRAWL_DATA WHERE `path`='/pc/selection/common/material_list' and id > 19739;
# select count(*) from (SELECT COUNT(bi.shop_id)as count, bi.shop_id from BUY_IN_01 bi group by bi.shop_id) a;
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
