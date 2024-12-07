import requests

json_data={
    "code": "risk.pre.loan.20241130213496", #路由，执行顺序
    "params":{
        "platformType":0,
        "storeCode":"dy001",
        "companyCode":"001"
    }
}
address = "http://121.40.223.55:7331"
result = requests.post(url=f"{address}/pandora-gateway/api/risk/check/execute", json=json_data)
print(result.status_code)
print(result.text)

# RC_2_DPYJGZ_1733209188848
# 店铺预警规则

{"errCode":1000,
 "errMsg":"success",
 "result":{
     "decisionCode":"2000",
     "decisionText":"店铺不可合作",
     "decisionType":1,
     "extraMap":{
         "suggest":"2000",
         "riskType":"2000",
         "decision":"2000",
         "priority":"500",
         "moreSuggest":"5000"}
 },"success":True}



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
# 店铺主营类目