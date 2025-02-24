import io
import os
import platform
import re
import sys
from datetime import datetime

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
    # 订单编号
    order_number_list = list()
    # 发货时间
    delivery_time_list = list()
    # 包裹状态
    package_status_list = list()

    excel = pd.ExcelFile(file_name)
    delivery_pd = pd.read_excel(excel, dtype={"订单编号": str, "发货时间": str, "当前状态": str})
    for t in delivery_pd.iterrows():
        index, row = t
        if isinstance(row["订单编号"], str) and isinstance(row["发货时间"], str):
            orders_number = row["订单编号"].split(",")
            date = row["发货时间"].split(" ")[0].strip()
            package_status = row["当前状态"].strip()
            # 包裹状态: 已运输待派件, 已签收, 待取件, 已派件待签收
            if package_status=="已运输待派件" or package_status=="已签收" or package_status=="待取件" or package_status=="已派件待签收":
                for order in orders_number:
                    order_number_list.append(order.strip())
                    delivery_time_list.append(date)
                    package_status_list.append(package_status)
    return {"订单编号": order_number_list, "发货时间": delivery_time_list, "当前状态": package_status_list}

# 待结算   /home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单在途资金导出.xlsx_182366450_1.xlsx
# 获取 订单号和预计结算金额（元）
def pending_settlement_fun(file_name: str) -> dict:
    order_dict = dict()
    excel = pd.ExcelFile(file_name)
    pending_pd = pd.read_excel(excel, dtype={"订单号": str, "预计结算金额（元）": str})
    for t in pending_pd.iterrows():
        index, row = t
        if isinstance(row["订单号"], str) and isinstance(row["预计结算金额（元）"], str):
            order_number = row["订单号"].strip()
            expected = row["预计结算金额（元）"].strip()
            if is_float(expected):
                order_dict.setdefault(order_number, expected)
            else:
                order_dict.setdefault(order_number, "0.00")
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
    order_number_list = list()
    # after_sales_list = list()
    # order_state_list = list()
    for t in order_pd.iterrows():
        # 订单状态: 交易成功, 已收货, 已发货
        # 售后状态: "", 退款关闭, 换货关闭
        index, row = t
        # if isinstance(row["订单号"], (str,int)):
        order_number = str(row["订单号"]).strip()
        after_sales_state = str(row["售后状态"]).strip()
        order_state = str(row["订单状态"]).strip()
        # print(order_number)
        if after_sales_state in ["", "退款关闭", "换货关闭"]:
            if order_state in  ["交易成功", "已收货", "已发货"]:
                order_number_list.append(order_number)
                # after_sales_list.append(after_sales_state)
                # order_state_list.append(order_state)

    # return {"订单编号": order_number_list, "售后状态": after_sales_list, "订单状态":order_state_list}
    return {"订单编号": order_number_list}



if __name__ == '__main__':
    deliver = deliver_fun(file_name="/home/james/Documents/2025.2.20原始数据/KS/快手-善行-包裹.xls")
    # print(deliver)
    order_management = order_management_fun(file_name ="/home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单管理.xlsx",
                                        password="b9cac4")
    # print(order_management)
    pending_settlement = pending_settlement_fun(file_name="/home/james/Documents/2025.2.20原始数据/KS/快手-善行-订单在途资金导出.xlsx_182366450_1.xlsx")

    # print(pending_settlement)

    order_number_deliver_set = set(deliver["订单编号"])
    # print(order_number_deliver_set)
    order_number_order_management_set = set(order_management["订单编号"])
    # print(order_number_order_management_set)
    order_number_pending_settlement_set = set(pending_settlement.keys())
    # print(order_number_pending_settlement_set)

    inner_set = order_number_deliver_set & order_number_order_management_set & order_number_pending_settlement_set
    print(inner_set)

    # order_m = order_management(file_name="/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-订单管理.csv")
    # assert len(order_m["子订单编号"]) == len(order_m["售后状态"])
    # # print(order_m)
    # deliver = deliver_fun("/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-包裹中心导出-2025-02-20 11-15-41.xlsx")
    # # print(deliver)
    # temp_order_number = list()
    # temp_deliver_time = list()
    # temp_package_status = list()
    # temp_after_sales = list()
    # for i in range(0, len(order_m["子订单编号"])):
    #     sub_order_number = order_m["子订单编号"][i]
    #     if sub_order_number in deliver["订单编号"]:
    #         for j in range(0, len(deliver["订单编号"])):
    #             order_number = deliver["订单编号"][j]
    #             if sub_order_number == order_number:
    #                 temp_order_number.append(sub_order_number)
    #                 temp_deliver_time.append(deliver["发货时间"][j])
    #                 temp_package_status.append(deliver["包裹状态"][j])
    #                 temp_after_sales.append(order_m["售后状态"][i])
    #
    # temp_d = {"订单编号": temp_order_number,
    #           "发货时间": temp_deliver_time,
    #           "包裹状态": temp_package_status,
    #           "售后状态": temp_after_sales}
    # print(len(temp_d["订单编号"]))
    # print(len(temp_d["发货时间"]))
    # print(len(temp_d["包裹状态"]))
    # print(len(temp_d["售后状态"]))
    # df = pd.DataFrame(temp_d)
    # df = df[(df['售后状态'] == '-') |
    #         (df['售后状态'] == '售后关闭') |
    #         (df['售后状态'] == '补寄成功')]
    # df = df[(df['包裹状态'] == '') |
    #         (df['包裹状态'] == '待取件') |
    #         (df['包裹状态'] == '派送中') |
    #         (df['包裹状态'] == '已揽收待中转') |
    #         (df['包裹状态'] == '已签收') |
    #         (df['包裹状态'] == '已中转待派件')]
    # df_dict = df.to_dict(orient='list')
    # # print(df_dict)
    # order_date_dict=dict()
    # for i in range(0, len(df_dict["订单编号"])):
    #     order_date_dict.setdefault(df_dict["订单编号"][i],df_dict["发货时间"][i])
    #
    #
    # order_account = pending_settlement("/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-待结算.csv")
    # deli_time = list()
    # prepend_account = list()
    # result_dict = dict()
    # for key in order_account.keys():
    #     for i in range(0, len(df_dict["订单编号"])):
    #         nu = df_dict["订单编号"][i]
    #         if key == nu:
    #             deli_time.append(df_dict["发货时间"][i])
    #             prepend_account.append(float(order_account[key]))
    #             print(nu, df_dict["发货时间"][i], order_account[key])

    # for key in set(order_account.keys()) & set(order_date_dict.keys()):
    #     deli_time.append(order_date_dict[key])
    #     prepend_account.append(float(order_account[key]))
    #     print(key, order_date_dict[key], order_account[key])
    #
    #
    # result_dict = {"发货时间": deli_time, "预计结算金额": prepend_account}
    # print(len(result_dict["发货时间"]))
    # df = pd.DataFrame(result_dict)
    # su = df.groupby("发货时间")["预计结算金额"].sum()
    # #
    # result = {
    #     "日期": list(su.index.values),
    #     "金额": list(su.values)
    # }
    # result_pd = pd.DataFrame(result)
    # print(result_pd)
    # print(f"预计结算金额 总额: {result_pd['金额'].sum()}")

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
