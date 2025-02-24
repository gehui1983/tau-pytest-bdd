import os
import platform
import re
import sys
from datetime import datetime

import pandas as pd
from pandas import Series


# 1. 抖音-百肤邦-订单管理.csv 和 抖音-百肤邦-包裹中心导出-2025-02-20 11-15-41.xlsx
# 计算
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


# 预计结算金额
expected_settlement_amount = list()


# data = {
#     "订单编号": order_number,
#     "发货时间": delivery_time,
#     "预计结算金额": expected_settlement_amount
# }


# 订单编号 函数
# 发货时间 函数
def deliver_fun(file_name: str) -> dict:
    # 订单编号
    order_number_list = list()
    # 发货时间
    delivery_time_list = list()
    # 包裹状态
    package_status_list = list()

    excel = pd.ExcelFile(file_name)
    delivery_pd = pd.read_excel(excel, dtype={"订单编号": str, "发货时间": str, "包裹状态": str})
    for t in delivery_pd.iterrows():
        index, row = t
        if isinstance(row["订单编号"], str) and isinstance(row["发货时间"], str):
            orders = row["订单编号"].split(",")
            date = row["发货时间"].split(" ")[0].strip()
            package_status = row["包裹状态"]
            for order in orders:
                order_number_list.append(order)
                delivery_time_list.append(date)
                package_status_list.append(package_status)
    return {"订单编号": order_number_list, "发货时间": delivery_time_list, "包裹状态": package_status_list}


def pending_settlement(file_name: str) -> dict:
    order_dict = dict()
    order_pd = pd.read_csv(file_name, chunksize=100, dtype={"子订单编号": str, "预计结算金额": str}, encoding="gbk")
    for t in order_pd:
        for index, row in t.iterrows():
            sub_order = row["子订单编号"].strip()
            expected = row["预计结算金额"].strip()
            if is_float(expected):
                order_dict.setdefault(sub_order, expected)
            else:
                order_dict.setdefault(sub_order, "0.00")
    return order_dict


# 订单管理
def order_management(file_name: str) -> dict:
    order_pd = pd.read_csv(file_name, chunksize=100, dtype={"子订单编号": str, "售后状态": str}, encoding="gbk")
    sub_order_list = list()
    after_sales_list = list()
    for t in order_pd:
        for index, row in t.iterrows():
            sub_order: str = row["子订单编号"].strip()
            after_sales: str = row["售后状态"].strip()
            after_sales_array = after_sales.split("-")
            after_sales_name = after_sales_array[len(after_sales_array) - 1]
            sub_order_array = sub_order.split(";")
            for s in sub_order_array:
                sub_order_list.append(s)
                if after_sales_name == "":
                    after_sales_name = "-"
                after_sales_list.append(after_sales_name)
    return {"子订单编号": sub_order_list, "售后状态": after_sales_list}


if __name__ == '__main__':
    order_m = order_management(file_name="/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-订单管理.csv")
    assert len(order_m["子订单编号"]) == len(order_m["售后状态"])
    # print(order_m)
    deliver = deliver_fun("/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-包裹中心导出-2025-02-20 11-15-41.xlsx")
    # print(deliver)
    temp_order_number = list()
    temp_deliver_time = list()
    temp_package_status = list()
    temp_after_sales = list()
    for i in range(0, len(order_m["子订单编号"])):
        sub_order_number = order_m["子订单编号"][i]
        if sub_order_number in deliver["订单编号"]:
            for j in range(0, len(deliver["订单编号"])):
                order_number = deliver["订单编号"][j]
                if sub_order_number == order_number:
                    temp_order_number.append(sub_order_number)
                    temp_deliver_time.append(deliver["发货时间"][j])
                    temp_package_status.append(deliver["包裹状态"][j])
                    temp_after_sales.append(order_m["售后状态"][i])

    temp_d = {"订单编号": temp_order_number,
              "发货时间": temp_deliver_time,
              "包裹状态": temp_package_status,
              "售后状态": temp_after_sales}
    print(len(temp_d["订单编号"]))
    print(len(temp_d["发货时间"]))
    print(len(temp_d["包裹状态"]))
    print(len(temp_d["售后状态"]))
    df = pd.DataFrame(temp_d)
    df = df[(df['售后状态'] == '-') |
            (df['售后状态'] == '售后关闭') |
            (df['售后状态'] == '补寄成功')]
    df = df[(df['包裹状态'] == '') |
            (df['包裹状态'] == '待取件') |
            (df['包裹状态'] == '派送中') |
            (df['包裹状态'] == '已揽收待中转') |
            (df['包裹状态'] == '已签收') |
            (df['包裹状态'] == '已中转待派件')]
    df_dict = df.to_dict(orient='list')
    # print(df_dict)
    order_date_dict=dict()
    for i in range(0, len(df_dict["订单编号"])):
        order_date_dict.setdefault(df_dict["订单编号"][i],df_dict["发货时间"][i])


    order_account = pending_settlement("/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-待结算.csv")
    deli_time = list()
    prepend_account = list()
    result_dict = dict()
    # for key in order_account.keys():
    #     for i in range(0, len(df_dict["订单编号"])):
    #         nu = df_dict["订单编号"][i]
    #         if key == nu:
    #             deli_time.append(df_dict["发货时间"][i])
    #             prepend_account.append(float(order_account[key]))
    #             print(nu, df_dict["发货时间"][i], order_account[key])

    for key in set(order_account.keys()) & set(order_date_dict.keys()):
        deli_time.append(order_date_dict[key])
        prepend_account.append(float(order_account[key]))
        print(key, order_date_dict[key], order_account[key])


    result_dict = {"发货时间": deli_time, "预计结算金额": prepend_account}
    print(len(result_dict["发货时间"]))
    df = pd.DataFrame(result_dict)
    su = df.groupby("发货时间")["预计结算金额"].sum()
    #
    result = {
        "日期": list(su.index.values),
        "金额": list(su.values)
    }
    result_pd = pd.DataFrame(result)
    print(result_pd)
    print(f"预计结算金额 总额: {result_pd['金额'].sum()}")

    # delivery_name = None
    # order_name = None
    #
    # if len(sys.argv) < 2:
    #     print(">>>>>缺少参数<<<<<")
    #     print("参数格式如下：")
    #     print("python douyin_order_match.py 物流表单.xlsx 订单表.csv 开始日期[2024-11-08] 结束日期[2024-11-09]")
    #     exit(0)
    # delivery_name = sys.argv[1]
    # print(delivery_name)
    # order_name = sys.argv[2]
    # print(order_name)
    #
    # # delivery_name = "/home/james/PycharmProjects/tau-pytest-bdd/xh/海乐威-包裹中心导出-2024-11-26 17-11-51.xlsx"
    # # order_name = "/home/james/PycharmProjects/tau-pytest-bdd/xh/海乐威-待结算订单.csv"
    #
    # names = []
    # if get_os_type() == "win":
    #     names = delivery_name.split("\\")
    # if get_os_type() == "linux":
    #     names = delivery_name.split("/")
    #
    # if len(names) == 0:
    #     exit(0)
    #
    # file_name = names[len(names) - 1]
    # store_name = file_name.split('-')[0]
    # print(store_name)
    # dir_name = delivery_name[0:len(delivery_name) - len(file_name)]
    # print(dir_name)
    #
    # deliver_fun(deliveryName=delivery_name)
    # order_fun(orderName=order_name)
    # assert len(data["订单编号"]) != len("发货时间")
    #
    # for o in data["订单编号"]:
    #     m = order_dict.get(o)
    #     if m is not None:
    #         data["预计结算金额"].append(float(m))
    #     else:
    #         data["预计结算金额"].append(0)
    # df = pd.DataFrame(data)
    # su = df.groupby("发货时间")["预计结算金额"].sum()
    #
    # # print(str(su))
    # # print(su.index.values)
    #
    # result = {
    #     "日期": list(su.index.values),
    #     "金额": list(su.values)
    # }
    # result_pd = pd.DataFrame(result)
    # print(result_pd)
    # print(f"预计结算金额 总额: {result_pd['金额'].sum()}")
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
