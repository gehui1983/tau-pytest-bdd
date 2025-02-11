import sys
from datetime import datetime

import pandas as pd
import re

import os
import platform


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


# def contains_chinese_re(text):
#     pattern = re.compile('[\u4e00-\u9fff]')
#     return bool(pattern.search(text))


# 订单号
order_number = list()
# 订单状态
order_number_status = list()
# 发货时间 MM/DD/YYYY
deliver_date = list()
# 售后状态
saled_status = list()
# 商家实收金额(元)
merchant_actual_received_amount = list()
order_data = {
    "订单号": order_number,
    "订单状态": order_number_status,
    "发货时间": deliver_date,
    "售后状态": saled_status,
    "商家实收金额(元)": merchant_actual_received_amount
}


# 订单号
def clear_order_number(f_source: list):
    for f in f_source:
        f = f.strip()
        order_number.append(f)


# 订单状态
def clear_order_number_status(f_source: list):
    # print(f_source)
    for f in f_source:
        f = f.strip()
        order_number_status.append(f)


# 发货时间
def clear_deliver_date(f_source: list):
    for f in f_source:
        # print(files"{type(files)}---{files}")
        if isinstance(f, str):
            # print(files)
            f = f.strip()
            if f == "\t":
                deliver_date.append("无发货时间")
            else:
                f = f.split(" ")[0]
                deliver_date.append(f)


# "售后状态"
def clear_saled_status(f_source: list):
    # print(f_source)
    for f in f_source:
        f = f.strip()
        saled_status.append(f)


# 商家实收金额
def clear_merchant_actual_received_amount(f_source: list):
    # print(f_source)
    for f in f_source:
        if isinstance(f, str):
            f = f.strip()
            if is_float(f):
                merchant_actual_received_amount.append(float(f))
            else:
                # print(files)
                merchant_actual_received_amount.append(float("0.00"))
        elif isinstance(f, float):
            merchant_actual_received_amount.append(f)
        elif isinstance(f, int):
            merchant_actual_received_amount.append(f)


if __name__ == '__main__':
    # if len(sys.argv) <= 1:
    #     print(">>>>>请输入文件路径<<<<<")
    #     exit(0)
    # csv_file = sys.argv[1]
    # csv_file = "/home/james/PycharmProjects/tau-pytest-bdd/xh/海乐威-待结算订单.csv"
    csv_file = "/home/james/Downloads/PDD/海乐威-订单管理.csv"
    names = []
    if get_os_type() == "win":
        names = csv_file.split("\\")
    if get_os_type() == "linux":
        names = csv_file.split("/")

    if len(names) == 0:
        exit(0)

    file_name = names[len(names) - 1]
    store_name = file_name.split('-')[0]
    # print(store_name)
    dir_name = csv_file[0:len(csv_file) - len(file_name)]
    # print(dir_name)

    df = pd.read_csv(csv_file)
    # print(df["订单号"])

    clear_order_number(f_source=df["订单号"])

    # print(order_number)
    clear_order_number_status(df["订单状态"])
    # print(order_number_status)

    clear_deliver_date(df["发货时间"])
    # print(deliver_date)

    clear_saled_status(df["售后状态"])
    # print(saled_status)

    clear_merchant_actual_received_amount(df["商家实收金额(元)"])
    # print(merchant_actual_received_amount)
    for i in range(0, len(saled_status)):
        if saled_status[i] == '退款成功' or saled_status[i] == '售后处理中':
            order_number_status[i] = "退款成功"

    df = pd.DataFrame(order_data)

    df = df[(df['订单状态'] == '已发货，待收货') | (df['订单状态'] == '已收货')]

    su = df.groupby("发货时间")["商家实收金额(元)"].sum()
    result = {
        "日期": list(su.index.values),
        "金额": list(su.values)
    }
    result_pd = pd.DataFrame(result)

    # print(result_pd)
    print(f"预计结算金额 总额: {result_pd['金额'].sum()}")
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H-%M-%S')

    with open(file=f"{dir_name}{store_name}-待结算订单汇总-{formatted_now}.txt", mode="wt") as files:
        files.write(f"总计：\r\n")
        files.write(str(result_pd))
        files.write(f"\r\n预计结算金额 总额: {result_pd['金额'].sum()}")
        if len(sys.argv) == 4:
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            files.write(f"\r\n\r\n 从{start_date}到{end_date}：\r\n")
            result_pd_0 = result_pd[(result_pd['日期'] >= start_date) & (result_pd['日期'] <= end_date)]
            print(result_pd_0)
            print(f"\r\n{start_date}到{end_date}预计结算金额: {result_pd_0['金额'].sum()}")
            files.write(str(result_pd_0))
            files.write(f"\r\n{start_date}到{end_date}预计结算金额: {result_pd_0['金额'].sum()}")
