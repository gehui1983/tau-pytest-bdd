import io
import os
import platform
import re
# import sys
# from datetime import datetime

import msoffcrypto
import pandas as pd


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

# 包裹 /home/james/Documents/2025.2.20原始数据/KS/快手-善行-包裹.xls
# 获取 订单号和发货日期，包裹状态
# 包裹状态: 已运输待派件, 已签收, 待取件, 已派件待签收
def deliver_fun(file_name: str) -> dict:

    deliver_dict = dict()
    excel = pd.ExcelFile(file_name)
    delivery_pd = pd.read_excel(excel, dtype={"订单编号": str, "发货时间": str, "当前状态": str})
    for t in delivery_pd.iterrows():
        index, row = t
        # if isinstance(row["订单编号"], str) and isinstance(row["发货时间"], str):
        order_number = str(row["订单编号"]).split(",")
        date = str(row["发货时间"]).split(" ")[0].strip()
        package_status = str(row["当前状态"]).strip()
        # 包裹状态: 已运输待派件, 已签收, 待取件, 已派件待签收
        if package_status in ["已运输待派件", "已签收", "待取件", "已派件待签收"]:
            for o in order_number:
                # order_number_list.append(o.strip())
                # delivery_time_list.append(date)
                # package_status_list.append(package_status)
                value = deliver_dict.get(o)
                if value is None:
                    deliver_dict.setdefault(o, [(date, package_status)])
                else:
                    assert isinstance(value, list)
                    value.append((date, package_status))
    # print("deliver_fun len:", len(order_number_list))
    # return {"订单编号": order_number_list, "发货时间": delivery_time_list, "当前状态": package_status_list}
    return deliver_dict

# 待结算   /home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单在途资金导出.xlsx_182366450_1.xlsx
# 获取 订单号和预计结算金额（元）
def pending_settlement_fun(file_name: str) -> dict:
    order_dict = dict()
    excel = pd.ExcelFile(file_name)
    pending_pd = pd.read_excel(excel, dtype={"订单号": str, "预计结算金额（元）": str})
    for t in pending_pd.iterrows():
        index, row = t
        order_number = str(row["订单号"]).strip()
        expected = str(row["预计结算金额（元）"]).strip()
        if not is_float(expected):
            expected = "0.00"
        values = order_dict.get(order_number)
        if values is None:
            order_dict.setdefault(order_number, [expected])
        else:
            assert isinstance(values, list)
            values.append(expected)
    print("pending_settlement_fun len:", len(order_dict.keys()))
    return order_dict


# 订单管理 /home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单管理.xlsx
# 获取 订单号, 售后状态, 订单状态
# 订单状态: 交易成功, 已收货, 已发货
# 售后状态: "", 退款关闭, 换货关闭
def order_management_fun(file_name: str, password:str) -> dict:
    file_temp = io.BytesIO()
    with open(file_name, "rb") as f:
        file = msoffcrypto.OfficeFile(f)
        # 判断是否有密码
        if file.is_encrypted():
            file.load_key(password)
            file.decrypt(file_temp)
        else:
            file_temp = file_name
    # 读取文件
    excel = pd.ExcelFile(file_temp)
    order_pd = pd.read_excel(excel, dtype={"订单号": str, "售后状态": str, "订单状态":str})
    order_dict = dict()

    for t in order_pd.iterrows():
        # 订单状态: 交易成功, 已收货, 已发货
        # 售后状态: "", 退款关闭, 换货关闭
        index, row = t
        # if isinstance(row["订单号"], (str,int)):
        order_number = str(row["订单号"]).strip()
        after_sales_state = str(row["售后状态"]).strip()
        if after_sales_state.lower() == "nan":
            after_sales_state=""
        order_state = str(row["订单状态"]).strip()
        if order_state.lower() == "nan":
            order_state = ""
        if (after_sales_state in ["", "退款关闭", "换货关闭"]) and (order_state in  ["交易成功", "已收货", "已发货"]):
            value = order_dict.get(order_number)
            if value is None:
                order_dict.setdefault(order_number, [(after_sales_state, order_state)])
            else:
                assert isinstance(value, list)
                value.append((after_sales_state, order_state))
    return order_dict


if __name__ == '__main__':
    deliver_d = deliver_fun(file_name="/home/james/Documents/2025.2.20原始数据/KS/快手-善行-包裹-01.xls")
    pending_d = pending_settlement_fun(file_name="/home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单在途资金导出.xlsx_182366450_1-01.xlsx")
    order_d = order_management_fun(
        file_name="/home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单管理-01.xlsx",
        password="b9cac4")

    inner_set = deliver_d.keys()  & pending_d.keys() & order_d.keys()
    print(inner_set)

    # 订单编号
    order_list = list()
    # 发货时间
    deliver_time_list = list()
    # 包裹状态
    pack_state_list = list()

    # 预计结算金额
    pending_account_list = list()
    # 售后状态
    saled_status_list = list()
    # 订单状态
    order_state_list = list()

    for order in inner_set:
        order_list.append(order)
        deliver_time, pack_state = deliver_d[order][0]
        deliver_time_list.append(deliver_time)
        pack_state_list.append(pack_state)
        saled_status, order_state = order_d[order][0]
        saled_status_list.append(saled_status)
        order_state_list.append(order_state)
        pending_account_list.append(float(pending_d[order][0]))

    result_dict = {"订单编号":order_list,
                   "发货时间": deliver_time_list,
                   "包裹状态": pack_state_list,
                   "预计结算金额":pending_account_list,
                   "售后状态":saled_status_list,
                   "订单状态":order_state_list
                   }
    print(len(result_dict["发货时间"]))
    print(result_dict["订单编号"])
    df = pd.DataFrame(result_dict)
    su = df.groupby("发货时间")["预计结算金额"].sum()
    result = {
        "日期": list(su.index.values),
        "金额": list(su.values)
    }
    result_pd = pd.DataFrame(result)
    print(result_pd)
    print(f"预计结算金额 总额: {result_pd['金额'].sum()}")
