import random
import datetime# 地区码表（示例，实际应包含所有有效地区码）
from typing import List, Optional, Any

# from typing import List, Optional, Type, Tuple

import pymysql as mysql


def query_district_code(host="127.0.0.1", parent_code="310100", level=3) -> Optional[list[Any]]:
    sql_select = '''SELECT code, name from CRAWL_DB0.distrit_code WHERE `parent_code` = %s and `level` = %s'''
    data = list()
    conn = mysql.connect(host=host, port=3306, user='admin',
                         password='admin', database="CRAWL_DB0")
    cur = conn.cursor()
    try:
        cur.execute(sql_select, [parent_code, level])
        res = cur.fetchall()
        for t in res:
            data.append(t)
    except mysql.MySQLError as e:
        print(e.args)
    finally:
        cur.close()
        conn.close()
    return data

def condition() -> tuple:
    area_codes = query_district_code()
    area_code = random.choice(area_codes)# 随机生成一个出生日期（例如1950年到2000年之间）
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2000, 12, 31)
    date_range = (end_date - start_date).days
    birth_date = start_date + datetime.timedelta(days=random.randint(0, date_range))
    birth_date = birth_date.strftime("%Y%m%d")# 随机生成顺序码
    order_code = f"{random.randint(00, 99):02d}"# 校验码计算函数
    sex_code = f"{random.randint(0, 9):1d}"
    return area_code, birth_date, order_code, sex_code
def calculate_check_digit(card_num):
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_digit_map = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    total = sum(int(card_num[i]) * factors[i] for i in range(17))
    digit = check_digit_map[total % 11]
    return digit
# 拼接前17位
if __name__ == "__main__":
    # 出生地:省，市，县或区
    # 出生日期：指定日期，指定年龄，随机
    # 性别：男，女
    # 姓名：无，随机
    # 生成数量
    # birth_pace = "湖北省|武汉市"
    # birth_date = datetime.date(1950, 1, 1)
    # sex = "F"
    # name = ""
    generate_num = 10
    for i in range(generate_num):
        area_code, birth_date, order_code, sex_code = condition()
        card_num = area_code[0] + birth_date + order_code + sex_code# 计算校验码
        check_digit = calculate_check_digit(card_num=card_num)# 拼接完整的身份证号码
        id_card_num = card_num + check_digit# 输出生成的身份证号码
        print(f'{area_code[1]}---{id_card_num}')
