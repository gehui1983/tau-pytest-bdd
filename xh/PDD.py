import os
import platform
import re
# import sys
# from datetime import datetime

import pandas as pd
from pandas import Series

# 文件：/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-包裹中心-01.csv
# 字段：订单号, 包裹状态
# 包裹状态:"已派件", "已签收", "转运中", "已揽件"

# 文件：/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-订单管理-01.csv
# 字段：订单号, 发货时间, 售后状态, 订单状态, 商家实收金额(元)
# 售后状态:无售后或售后取消
# 订单状态:"已发货", "待收货", "已收货"

#实现方式：
# 一、包裹中心处理 实现 步骤：
    # 1.包裹中心 获取 "订单号", "包裹状态"
    # 2.通过 包裹状态(字段)【"已派件", "已签收", "转运中", "已揽件"】过滤出, 订单号
    # 3.返回：采用字典,key为订单号，value为list， list内容为包裹状态
# 二、订单管理处理 实现 【同理：包裹中心处理】
# 三、计算 “订单管理处理 返回的 订单号” 和 “包裹中心处理 返回的 订单号” 集合交集 inner_set
# 四、接上一步，根据 inner_set 计算 出 “订单号, 发货时间, 售后状态, 订单状态, 商家实收金额(元)”


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


# 文件：/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-包裹中心-01.csv
# 字段：订单号, 包裹状态
# 包裹状态:"已派件", "已签收", "转运中", "已揽件"
def deliver_fun(filepath_or_buffer: str) -> dict:

    delivery_pd = pd.read_csv(filepath_or_buffer = filepath_or_buffer, chunksize=100,
                              dtype={"订单号": str, "包裹状态": str})
    deliver_dict = dict()
    for t in delivery_pd:
        for index, row in t.iterrows():
            order_number = str(row["订单号"]).strip()
            package_state = str(row["包裹状态"]).strip()
            if package_state.lower() == 'nan':
                package_state = ""
            if package_state in ["已派件", "已签收", "转运中", "已揽件"]:
                value = deliver_dict.get(order_number)
                if value is None:
                    deliver_dict.setdefault(order_number,[package_state])
                else:
                    assert isinstance(value, list)
                    value.append(package_state)
    return deliver_dict


# 文件：/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-订单管理-01.csv
# 字段：订单号, 发货时间, 售后状态, 订单状态, 商家实收金额(元)
# 售后状态:无售后或售后取消
# 订单状态:"已发货", "待收货", "已收货"
def order_fun(filepath_or_buffer: str) -> dict:
    order_pd = pd.read_csv(filepath_or_buffer=filepath_or_buffer, chunksize=100,
                           dtype={"订单号": str, "发货时间":str, "订单状态": str,"售后状态":str, "商家实收金额(元)": str})

    order_manager_dict = dict()
    for t in order_pd:
        for index, row in t.iterrows():
            order_number = str(row["订单号"]).strip()
            goods_time = str(row["发货时间"]).strip().split(" ")[0].strip()
            order_state = str(row["订单状态"]).strip()
            saled_state = str(row["售后状态"]).strip()
            actual_amount = str(row["商家实收金额(元)"]).strip()
            if is_float(actual_amount):
                actual_amount = actual_amount
            else:
                actual_amount = "0.00"

            if (order_state in ["已发货，待收货","已收货"]) and (saled_state in ["无售后或售后取消"]):

                d = order_manager_dict.get(order_number)
                if d is None:
                    order_manager_dict.setdefault(order_number, [(goods_time, order_state, saled_state, actual_amount)])
                else:
                    assert isinstance(d, list)
                    d.append((goods_time, order_state, saled_state, actual_amount))

    return order_manager_dict

if __name__ == '__main__':
    delivery_file_name = "/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-包裹中心-01.csv"
    deliver_dict = deliver_fun(filepath_or_buffer=delivery_file_name)
    order_file_name = "/home/james/Documents/2025.2.20原始数据/PDD/拼多多-百肤邦-订单管理-01.csv"
    order_dict = order_fun(filepath_or_buffer=order_file_name)
    inner_sets = order_dict.keys() & deliver_dict.keys()

    print(inner_sets)

    # 订单号
    order_number_list = list()
    # 发货时间
    goods_time_list = list()
    # 订单状态
    order_state_list = list()
    # 售后状态
    saled_state_list = list()
    # 商家实收金额(元)
    actual_amount_list = list()
    # 包裹状态
    deliver_state_list = list()

    for order in inner_sets:
        order_number_list.append(order)
        values = order_dict.get(order)
        goods_time, order_state, saled_state, actual_amount = values[0]
        goods_time_list.append(goods_time)
        order_state_list.append(order_state)
        saled_state_list.append(saled_state)
        actual_amount_list.append(float(actual_amount))
        deliver_state_list.append(deliver_dict[order][0])


    # "订单号":order_number_list,
    # "发货时间"，"订单状态"，"售后状态","商家实收金额(元)" 列表长度和 订单号 列表长度相同
    length =  len(order_number_list)
    assert len(goods_time_list) == length
    assert len(saled_state_list) == length
    assert len(order_state_list) == length
    assert len(actual_amount_list) == length
    data = {
        "订单号":order_number_list,
        "发货时间":goods_time_list,
        "订单状态":order_state_list,
        "售后状态":saled_state_list,
        "商家实收金额(元)": actual_amount_list,
        "包裹状态": deliver_state_list
    }
    df = pd.DataFrame(data)
    su: Series = df.groupby("发货时间")["商家实收金额(元)"].sum()

    result = {
        "日期": list(su.index.values),
        "金额": su.to_list()
    }
    result_pd = pd.DataFrame(result)
    print(result_pd)
    print(f"预计结算金额 总额: {result_pd['金额'].sum()}")