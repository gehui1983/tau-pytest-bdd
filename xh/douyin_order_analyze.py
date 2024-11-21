# encoding=utf-8
import sys
import pandas as pd
import re


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
        f = f.strip()
        if is_float(f):
            expected_settlement_amount.append(float(f))
        else:
            # print(f)
            expected_settlement_amount.append(float("0.00"))


# 预计结算日期函数
def clear_expected_settlement_date(f_source: list):
    for f in f_source:
        f = f.strip()
        expected_settlement_date.append(f)


if __name__ == '__main__':
    csv_file = sys.argv[1]
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
    print(str(su))
    # print(su.axes[0])

    co = df['预计结算金额'].sum()
    print(f"预计结算金额 总额: {co}")
