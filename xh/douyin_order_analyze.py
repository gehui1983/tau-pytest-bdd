# encoding=utf-8
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


# 退款状态
refund_status = list()

# 订单状态
order_status = list()

# 预计结算金额
expected_settlement_amount = list()

# 预计结算日期
expected_settlement_date = list()

data = {
    "退款状态": refund_status,
    "订单状态": order_status,
    "预计结算金额": expected_settlement_amount,
    "预计结算日期": expected_settlement_date
}


def clear_field(field):
    pass


# 退款状态函数
def clear_refund_status(f_source: list):
    for f in f_source:
        f = str(f).lower()
        if f == "nan":
            f = ""
        else:
            f = f.strip()
        refund_status.append(f)


# 订单状态函数
def clear_order_status(f_source: list):
    # print(f_source)
    for f in f_source:
        f = f.strip()
        order_status.append(f)


# 预计结算金额函数
def clear_expected_settlement_amount(f_source: list):
    # print(f_source)
    for f in f_source:
        if isinstance(f, str):
            f = f.strip()
            if is_float(f):
                expected_settlement_amount.append(float(f))
            else:
                # print(f)
                expected_settlement_amount.append(float("0.00"))
        elif isinstance(f, float):
            expected_settlement_amount.append(f)
        elif isinstance(f, int):
            expected_settlement_amount.append(f)


# 预计结算日期函数
def clear_expected_settlement_date(f_source: list):
    for f in f_source:
        # print(f"{type(f)}---{f}")
        if isinstance(f, str):
            f = f.strip()
            expected_settlement_date.append(f)
        elif isinstance(f, (float, int)):
            expected_settlement_date.append("无预计结算日期")
        # elif isinstance(f, int):
        #     expected_settlement_date.append(str(f).strip())


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print(">>>>>请输入文件路径<<<<<")
        exit(0)
    csv_file = sys.argv[1]
    # csv_file = "/home/james/PycharmProjects/tau-pytest-bdd/xh/海乐威-待结算订单.csv"
    names=[]
    if get_os_type() == "win":
        names = csv_file.split("\\")
    if get_os_type() == "linux":
        names = csv_file.split("/")

    if len(names)==0:
        exit(0)

    file_name = names[len(names)-1]
    store_name = file_name.split('-')[0]
    print(store_name)
    dir_name = csv_file[0:len(csv_file) - len(file_name)]
    print(dir_name)

    df = pd.read_csv(csv_file)
    clear_refund_status(f_source=df["退款状态"])
    # print(refund_status)
    clear_order_status(f_source=df["订单状态"])
    # print(order_status)
    clear_expected_settlement_amount(f_source=df["预计结算金额"])
    # print(expected_settlement_amount)

    clear_expected_settlement_date(f_source=df["预计结算日期"])
    # print(expected_settlement_date)

    df = pd.DataFrame(data)

    df = df[(df['退款状态'] == '')]
    df = df[(df["订单状态"] == "已发货") | (df["订单状态"] == "已完成")]

    su = df.groupby("预计结算日期")["预计结算金额"].sum()
    result = {
        "日期": list(su.index.values),
        "金额": list(su.values)
    }
    result_pd = pd.DataFrame(result)

    print(result_pd)

    print(f"预计结算金额 总额: {result_pd['金额'].sum()}")
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H-%M-%S')

    with open(file=f"{dir_name}{store_name}-待结算订单汇总-{formatted_now}.txt", mode="wt") as f:
        f.write(str(result_pd))
        f.write(f"\r\n预计结算金额 总额: {result_pd['金额'].sum()}")

