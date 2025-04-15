from dataclasses import make_dataclass

import numpy as np
import pandas as pd

# info_list =["毛晓明", "1", "310115199802102548","5000"]
# info_lists = list()
# info_lists.append(info_list)
# info_lists.append(info_list)
#
# data = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)],
#                 dtype=[("a", "i4"), ("b", "i4"), ("c", "i4")])
# df3 = pd.DataFrame(data, columns=['c', 'a'])
# [("毛晓明", "1", "310115199802102548","5000"), ("毛晓明", "2", "310115199802102548","5000")],

# data = np.array(info_lists)
# df1 = pd.DataFrame(data=data, columns=["被保险人姓名", "被保险人证件类型", "被保险人证件号", "初始个人额度"])
# [["毛晓明", "1", "310115199802102548","5000"], ["毛晓明", "2", "310115199802102548","5000"]]
# df1 = pd.DataFrame(data=info_lists,
#                    columns=["被保险人姓名", "被保险人证件类型", "被保险人证件号", "初始个人额度"],
#                    )
# ,mode="a",if_sheet_exists="overlay",


# Point = make_dataclass("Point", [("x", int), ("y", int)])
Point = make_dataclass("Point", [("被保险人姓名", str),
                                 ("被保险人证件类型", int), ("被保险人证件号", str), ("初始个人额度", int)])
l =  [Point("毛晓明", 1, "310115199802102548",5000),
      Point("毛晓明", 2, "310115199802102548",5000)]
df1 = pd.DataFrame(data=l)
with pd.ExcelWriter("/home/james/Downloads/pk/个人专属额度-初始化_0.xlsx",
                    engine="openpyxl",) as writer:
    df1.to_excel(writer, sheet_name="Sheet1", index=False)  # doctest: +SKIP