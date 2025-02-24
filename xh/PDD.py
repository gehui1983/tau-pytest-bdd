import os
import platform
import re
import sys
from datetime import datetime

import pandas as pd
from pandas import Series

from xh.ks_order_analyze import order_status


def get_os_type():
    if os.name == 'nt':
        return 'win'
    elif os.name == 'posix':
        if 'darwin' in platform.system().lower():
            return 'macOS'
        else:
            return 'linux'
    else:
        return 'unknown'


def is_float(s: str):
    pattern = r'-?\d+(\.\d+)?([eE][+-]?\d+)?$'
    if bool(re.match(pattern, s)):
        try:
            float(s)
            return True
        except ValueError:
            return False
    return False


# 订单编号
order_number = list()

# 发货时间
delivery_time = list()

# 商家实收金额(元)
expected_settlement_amount = list()

data = {
    "订单号": order_number,
    "发货时间": delivery_time,
    "商家实收金额(元)": expected_settlement_amount
}


# 订单编号 函数
# 发货时间 函数
def deliver_fun(deliveryName: str):
    global order0
    delivery_pd = pd.read_csv(deliveryName, dtype={"订单号": str, "发货时间": str, "包裹状态": str})
    for t in delivery_pd.iterrows():
        index, row = t
        order = str(row["订单号"]).strip()
        date = str(row["发货时间"]).split(" ")[0].strip()
        package = str(row["包裹状态"]).split(" ")[0].strip()
        if package in ["已派件", "已签收", "转运中", "已揽件"]:
            order_number.append(order)
            delivery_time.append(date)


order_dict = dict()


def order_fun(orderName: str):
    order_pd = pd.read_csv(orderName, chunksize=100, dtype={"订单号": str, "订单状态": str,"商家实收金额(元)": str})
    for t in order_pd:
        for index, row in t.iterrows():
            sub_order = str(row["订单号"]).strip()
            expected = str(row["商家实收金额(元)"]).strip()
            order_state = str(row["订单状态"]).strip()
            if order_state in ["已发货，待收货","已收货"]:
                if is_float(expected):
                    order_dict.setdefault(sub_order, expected)
                else:
                    order_dict.setdefault(sub_order, "0.00")


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print(">>>>>缺少参数<<<<<")
    #     print("参数格式如下：")
    #     print("python douyin_order_match.py 物流表单.xlsx 订单表.csv 开始日期[2024-11-08] 结束日期[2024-11-09]")
    #     exit(0)
    # delivery_name = sys.argv[1]
    # print(delivery_name)
    # order_name = sys.argv[2]
    # print(order_name)

    # delivery_name = "./PDD/海乐威-包裹中心.csv"
    # order_name = "./PDD/海乐威-订单管理.csv"
    delivery_name = "/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-包裹中心-01.csv"
    order_name = "/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-订单管理-01.csv"
    names = []
    if get_os_type() == "win":
        names = delivery_name.split("\\")
    if get_os_type() == "linux":
        names = delivery_name.split("/")

    if len(names) == 0:
        exit(0)

    file_name = names[len(names) - 1]
    store_name = file_name.split('-')[0]
    print(store_name)
    dir_name = delivery_name[0:len(delivery_name) - len(file_name)]
    print(dir_name)

    deliver_fun(deliveryName=delivery_name)
    order_fun(orderName=order_name)
    assert len(data["订单号"]) == len(data["发货时间"])

    for o in data["订单号"]:
        m = order_dict.get(o)
        if m is not None:
            data["商家实收金额(元)"].append(float(m))
        else:
            data["商家实收金额(元)"].append(0)
    df = pd.DataFrame(data)
    su: Series = df.groupby("发货时间")["商家实收金额(元)"].sum()

    result = {
        "日期": list(su.index.values),
        "金额": list(su.values)
    }
    result_pd = pd.DataFrame(result)
    print(result_pd)
    print(f"预计结算金额 总额: {result_pd['金额'].sum()}")
    # now = datetime.now()
    # formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
    # with open(file=f"{dir_name}{store_name}-待结算订单和包裹匹配汇总-{formatted_now}.txt", mode="wt") as f:
    #     f.write(str(result_pd))
    #     f.write(f"\n预计结算金额 总额: {result_pd['金额'].sum()}")
    #
    #     if len(sys.argv) == 5:
    #         start_date = sys.argv[3]
    #         end_date = sys.argv[4]
    #
    #         # start_date = '2024-11-08'
    #         # end_date = '2024-11-15'
    #         result_pd_0 = result_pd[(result_pd['日期'] >= start_date) & (result_pd['日期'] <= end_date)]
    #
    #         print(f'\n从{start_date}到{end_date} 详情')
    #         print(result_pd_0)
    #         print(f'从{start_date}到{end_date} 金额汇总：{result_pd_0["金额"].sum()}')
    #         f.write(f'\n从{start_date}到{end_date} 详情')
    #         f.write(str(result_pd_0))
    #         f.write(f'\n从{start_date}到{end_date} 金额汇总：{result_pd_0["金额"].sum()}')
