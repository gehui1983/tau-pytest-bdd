import re
import sys
import pandas as pd


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

# 预计结算金额
expected_settlement_amount = list()

data = {
    "订单编号": order_number,
    "发货时间": delivery_time,
    "预计结算金额": expected_settlement_amount
}


# 订单编号 函数
# 发货时间 函数
def deliver_fun(deliveryName: str):
    excel = pd.ExcelFile(deliveryName)
    delivery_pd = pd.read_excel(excel, dtype={"订单编号":str, "发货时间": str})
    for t in delivery_pd.iterrows():
        index, row = t
        # print(row["订单编号"])
        #
        # print(row)
        # print(f'{index}--{row["订单编号"]}---{row["发货时间"]}')
        if isinstance(row["订单编号"], str) and isinstance(row["发货时间"], str):
            orders = row["订单编号"].split(",")
            date = row["发货时间"].split(" ")[0].strip()
            for order in orders:
                order_number.append(order)
                delivery_time.append(date)


order_dict = dict()


def order_fun(orderName: str):
    order_pd = pd.read_csv(orderName, chunksize=100, dtype={"子订单编号": str, "预计结算金额": str})
    for t in order_pd:
        for index, row in t.iterrows():
            sub_order = row["子订单编号"].strip()
            expected = row["预计结算金额"].strip()
            if is_float(expected):
                order_dict.setdefault(sub_order, expected)
            else:
                order_dict.setdefault(sub_order, "0.00")


if __name__ == '__main__':
    # delivery_name = sys.argv[1]
    # order_name = sys.argv[2]
    delivery_name = "/Users/gehui/Downloads/包裹中心导出-2024-11-26 17-11-51.xlsx"
    order_name = "/Users/gehui/Downloads/1732612129_d0dfbc4c3c009f19957a2fcaf91098camlyBQLQo.csv"
    deliver_fun(deliveryName=delivery_name)
    order_fun(orderName=order_name)
    assert len(data["订单编号"]) != len("发货时间")

    for o in data["订单编号"]:
        m = order_dict.get(o)
        if m is not None:
            data["预计结算金额"].append(float(m))
        else:
            data["预计结算金额"].append(0)
    df = pd.DataFrame(data)
    su = df.groupby("发货时间")["预计结算金额"].sum()
    print(str(su))
    co = df['预计结算金额'].sum()
    print(f"预计结算金额 总额: {co}")
