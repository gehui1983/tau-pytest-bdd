import requests

json_data={
    "code": "risk.pre.loan.20241130213496",
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
