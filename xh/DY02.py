import os
import platform
import re
import sys
import chardet
import pandas as pd

def detect_file_encoding(file_path:str) -> str:
    with open(file_path, 'rb') as f:
        encoding = chardet.detect(f.read(100))['encoding']
        if encoding.lower()=="gb2312":
            encoding = "gbk"
        return encoding


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


# 包裹处理：
# 文件：/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-包裹中心导出-2025-02-20 11-15-41.xlsx
# 提取字段:订单编号, 发货时间, 包裹状态
def deliver_fun(file_name: str) -> dict:
    deliver_dict=dict()
    excel = pd.ExcelFile(file_name)
    delivery_pd = pd.read_excel(excel, engine='openpyxl', dtype={"订单编号": str, "发货时间": str, "包裹状态": str})
    for t in delivery_pd.iterrows():
        index, row = t
        orders = str(row["订单编号"]).split(",")
        date = str(row["发货时间"]).split(" ")[0].strip()
        package_status = str(row["包裹状态"])
        if package_status in ["", '待取件', '派送中', '已揽收待中转', '已签收', '已中转待派件']:
            for order in orders:
                values = deliver_dict.get(order)
                if values is None:
                    deliver_dict.setdefault(order,[(date, package_status)])
                else:
                    assert isinstance(values, list)
                    values.append((date, package_status))
    return deliver_dict

# 待结算：

def pending_settlement(file_name: str) -> dict:
    encoding = detect_file_encoding(file_path=file_name)
    order_pd = pd.read_csv(file_name, chunksize=3000, dtype={"子订单编号": str, "预计结算金额": str}, encoding=encoding)
    order_dict = dict()
    for t in order_pd:
        for index, row in t.iterrows():
            sub_order = row["子订单编号"].strip()
            expected = row["预计结算金额"].strip()
            if not is_float(expected):
                expected = "0.00"

            value = order_dict.get(sub_order)
            if value is None:
                order_dict.setdefault(sub_order, [expected])
            else:
                assert isinstance(value, list)
                value.append(expected)
    return order_dict


# 订单管理
def order_management(file_name: str) -> dict:
    print("---Detect Start-----")
    encoding = detect_file_encoding(file_path=file_name)
    print(encoding)
    # GB2312
    print("---Detect Start-----")
    order_pd = pd.read_csv(file_name, chunksize=3000, dtype={"子订单编号": str, "订单状态": str,"售后状态": str},
                           encoding=encoding)
    oder_dict = dict()
    for t in order_pd:
        for index, row in t.iterrows():
            sub_order = str(row["子订单编号"]).strip()
            after_sales = str(row["售后状态"]).strip()
            order_state = str(row["订单状态"]).strip()
            after_sales_array = after_sales.split("-")
            after_sales_name = after_sales_array[len(after_sales_array) - 1]
            if after_sales_name == "":
                after_sales_name = "-"
            if after_sales_name in ['-', '售后关闭', '补寄成功']:
                sub_order_array = sub_order.split(";")
                for s in sub_order_array:
                    value = oder_dict.get(s)
                    if value is None:
                        oder_dict.setdefault(s,[(after_sales_name,order_state)])
                    else:
                        assert isinstance(value, list)
                        value.append((after_sales_name,order_state))
    return oder_dict


def final_dy(deliver_name:str, order_name:str, pending_name:str) -> dict:
    # dtype = {"订单编号": str, "发货时间": str, "包裹状态": str})
    deliver_d = deliver_fun(file_name=deliver_name)
    deliver_set = deliver_d.keys()
    # dtype = {"子订单编号": str, "预计结算金额": str}
    pending_d = pending_settlement(file_name=pending_name)
    pending_set = pending_d.keys()
    # dtype = {"子订单编号": str, "售后状态": str}
    order_d = order_management(file_name=order_name)


    order_set = order_d.keys()

    inner_set = deliver_set & pending_set & order_set

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



    for order_num in inner_set:
        order_list.append(order_num)
        deliver_time, pack_state = deliver_d[order_num][0]
        deliver_time_list.append(deliver_time)
        pack_state_list.append(pack_state)

        pending_account_list.append(float(pending_d[order_num][0]))

        saled_status, order_state = order_d[order_num][0]
        saled_status_list.append(saled_status)
        order_state_list.append(order_state)
    result_dict = {"订单编号": order_list,
                   "发货时间": deliver_time_list,
                   "包裹状态": pack_state_list,
                   "预计结算金额": pending_account_list,
                   "售后状态": saled_status_list,
                   "订单状态": order_state_list
                   }
    print(len(result_dict["发货时间"]))
    return result_dict

# 结算单:/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-结算单.csv
def settlement_process(file_name:str) ->dict:
    print("---Detect Start-----")
    encoding = detect_file_encoding(file_path=file_name)
    print(encoding)
    # GB2312
    print("---Detect Start-----")
    p = r'\d+'
    settlement_pd = pd.read_csv(file_name, chunksize=3000, dtype={"子订单号": str, "结算金额": str},
                           encoding=encoding)
    result_dict = dict()
    for t in settlement_pd:
        for index, row in t.iterrows():
            # if row["子订单号"]
            # print(row["子订单号"], row["结算金额"])
            sub_order=re.findall(p, row["子订单号"])

            if len(sub_order) == 0:
                continue
            order = sub_order[0]
            account=row["结算金额"].strip()
            value = result_dict.get(order)
            if value is None:
                result_dict.setdefault(order, [account])
            else:
                assert isinstance(value,list)
                value.append(account)
    return result_dict

if __name__ == '__main__':
    deliver_name = "/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-包裹中心导出-2025-02-20 11-15-41.xlsx"
    order_name = "/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-订单管理.csv"
    pending_name = "/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-待结算.csv"
    settlement_name = "/home/james/Documents/2025.2.20原始数据/DY/抖音-百肤邦-结算单.csv"
    # if len(sys.argv) < 3:
    #     print(">>>>>缺少参数<<<<<")
    #     print("参数格式如下：")
    #     print("python DY01.py 物流表单.xlsx 订单表.csv 待结算.csv")
    #     exit(0)
    # deliver_name = sys.argv[1]
    # print("包裹: ", deliver_name)
    # order_name = sys.argv[2]
    # print("订单: ", order_name)
    # pending_name = sys.argv[3]
    # print("待结算", pending_name)

    result_dict = final_dy(deliver_name=deliver_name, order_name=order_name, pending_name=pending_name)

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

    # 结算金额
    settlement_list = list()
    settlement_d = settlement_process(file_name=settlement_name)
    order_list = df["订单编号"].to_list()
    settlement_order_list = list()
    for order_num in order_list:
        settlement_account = settlement_d.get(order_num)
        if settlement_account is None:
            pass
        else:
            settlement_order_list.append(order_num)
            settlement_list.append(float(settlement_account[0]))

    result_pd_0 = pd.DataFrame({"实际结算金额":settlement_list, "订单号":settlement_order_list})
    print(f'实际结算金额 总额：{result_pd_0["实际结算金额"].sum()}')
