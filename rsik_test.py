import codecs
import json
from datetime import datetime

import requests

json_data = {
    "code": "risk.pre.loan.20241130213496",  # 路由，执行顺序
    "params": {
        "platformType": 0,
        "storeCode": "dy001",
        "companyCode": "001"
    }
}
address = "https://rde.xhdigit.com"
result = requests.post(url=f"{address}/pandora-gateway/api/risk/check/execute", json=json_data)
print(result.headers)
t = result.text
print(t)
json_d = json.loads(t)
data_format = json.dumps(json_d, indent=4, ensure_ascii=False)
print(data_format)
now = datetime.now()
formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
with open(file=f"{formatted_now}.txt", mode="wt") as f:
    f.write(data_format)

# RC_2_DPYJGZ_1733209188848
# 店铺预警规则

{"errCode": 1000,
 "errMsg": "success",
 "result": {
     "decisionCode": "2000",
     "decisionText": "店铺不可合作",
     "decisionType": 1,
     "extraMap": {
         "suggest": "2000",
         "riskType": "2000",
         "decision": "2000",
         "priority": "500",
         "moreSuggest": "5000"}
 }, "success": True}

# {
# 	"errCode":1000,
# 	"errMsg":"success",
# 	"result":{
# 		"decisionCode":"3000",
# 		"decisionText":"OP&飞书预警",
# 		"decisionType":1,
# 		"extraMap":{
# 			"riskType":"2000",
# 			"decision":"3000",
# 			"priority":"500"
# 			}
# 		},
# 	"success":True
# }


# {
#     "errCode":1000,
#     "errMsg":"success",
#     "result":{
#         "decisionCode":"1000",
#         "decisionText":"通过",
#         "decisionType":0,
#         "extraMap":{}},
#     "success":True
# }

# redis-cli -h r-bp1uxwil4bql9mvfjspd.redis.rds.aliyuncs.com   6379
# xhdigit_dev Xh1016#$%

# Event_DPFXSJ_1732450735305

# $11 cateType==5
#
# $10 cateType==4
#
# $9  cateType==3

# $11 || $10 || $9
#


# 店铺基础信息
# 店铺主营类目isAccountChanged		是否店铺银行账户发生变更	true
# returnGoodsRat90d		            商品退货率				0.67
# isPunishChanged			        是否被惩戒(惩戒中心)		true
# fundsNeedAmount30d		        月资金需求金额			    6538322
# repayAmount90d			        近3个月平均月回款金额		456
# settledAmount30d		            结算客单价				347545
# cateType				            店铺主营类目				2
# storeDuration			            店铺经营时长				46
# storeExperienceScore	            店铺体验分				23
# platformType			            开店平台					0
# storeCode				            店铺ID					dy001
