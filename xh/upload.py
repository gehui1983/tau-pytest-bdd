import json
import time
import uuid

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pymysql as mysql


class mysql_op:
    def __init__(self,
                 store_ids: str,  # 店铺 ID
                 db_name: str = 'fin_portal_pre'
                 ):
        self.store_ids = store_ids  # 店铺ID 唯一 rm-bp1t4k5l69f6ifql5to.mysql.rds.aliyuncs.com
        self.db = mysql.connect(host="rm-bp1t4k5l69f6ifql5to.mysql.rds.aliyuncs.com", port=3306, user='xhadmin',
                                password='test#202412', database=db_name)
        self.cur = self.db.cursor()

    def select_audit_id(self, status: int):
        try:
            self.cur.execute('''select id from audit_info ai 
                                where ai.store_id = (select id from crm_store cs where cs.code = %s) 
                                and ai.status = %s''', [self.store_ids, status])
            audit_id = self.cur.fetchone()[0]
        except mysql.MySQLError as e:
            print(e.args)
        finally:
            self.cur.close()
            self.db.close()
        return audit_id

    def select_store_id(self):
        try:
            self.cur.execute('''select id from crm_store cs where cs.code = %s''', self.store_ids)
            id_int = self.cur.fetchone()[0]
        except mysql.MySQLError as e:
            print(e.args)
        finally:
            self.cur.close()
            self.db.close()
        return id_int


def upload_attachment(files: str, hosts: str, types: str, fileType: str, headers: dict) -> dict:
    urls = hosts + '/fin-portal/controller/customer/attachment/upload'
    with open(files, 'rb') as fd:
        fields = {
            'multipartFile': (files, fd, fileType),
            'type': types
        }
        form_data = MultipartEncoder(fields=fields, boundary=None)

        headers['Content-Type'] = form_data.content_type
        response = requests.post(url=urls, data=form_data, headers=headers)

    return json.loads(response.content)


def storeType_config(host: str, headers: dict) -> dict:
    url = host + '/fin-portal/controller/customer/config/storeType_config'
    response = requests.get(url=url, headers=headers)
    return json.loads(response.content)


def platformType_config(host: str, headers: dict) -> dict:
    url = host + '/fin-portal/controller/customer/config/platformType_config'
    response = requests.get(url=url, headers=headers)
    return json.loads(response.content)


# post http://120.27.128.65:7771/fin-portal/controller/customer/enterprise/create
def enterprise_create(host: str, headers: dict, store_id: int):
    headers["content-type"] = "application/json"
    url = host + "/fin-portal/controller/customer/enterprise/create"
    enterprise = {
        "id": 24,
        # 店铺数据id
        "storeId": store_id,
        "mobile": "13890809999",
        "name": "杭州电子",
        "code": "98491832579",
        "registerDate": "2025-01-27 00:00:00",
        "licenseAttachmentId": 774,
        "legalName": "Ihf",
        "legalCardNo": "9874918759791753987X",
        "legalMobile": ["98173498419"],
        "legalFrontAttachmentId": 778,
        "legalBackAttachmentId": 779,
        "legalCreditAttachmentId": [783],
        "enterpriseAttachmentId": [],
        "adminName": "杭州",
        "adminCardNo": "09840984508914038514X",
        "adminMobile": ["13800909090"],
        "adminFrontAttachmentId": 776,
        "adminBackAttachmentId": 777,
        "adminCreditAttachmentId": [],
        "shareholder": "[{\"type\":1,\"enterprise\":{\"code\":\"3256773\",\"creditAttachmentId\":[784],\"name\":\"杭州投资公司\"}}]",
        "declareType": [2],
        "accountNo": "0324820945",
        "accountName": "gehui",
        "bankName": "工商银行",
        "accountRecordAttachmentId": [788],
        "companyFinAttachmentId": [789],
        "taxAttachmentId": [790]
    }
    response = requests.post(url=url, headers=headers, json=enterprise)
    return response.content




def store_create(host: str, headers: dict, name: str, code: str) -> bytes:
    headers["content-type"] = "application/json"
    url = host + "/fin-portal/controller/customer/store/create"

    store_data = {
        # 店铺名称
        "name": name,
        # 店铺ID
        "code": code,
        # 店铺链接
        "url": "www.doundian.com",
        # 店铺类型
        "type": 0,
        # 开店时间
        "registerDate": "2025-01-01 00:00:00",
        # 经营品类
        "cateType": "服装",
        # 开店平台
        "platformType": 1,
        # 收款账户开户名
        "accountName": "开户名",
        # 收款账户开户行
        "bankName": "中国银行",
        # 收款账号
        "accountNo": "94179874957514957978435",
        # 计息方式
        # 按日计息
        "billingMethodType": "1",
        # 服务费率（%）
        "billingMethodValue": "1",
        # 综合账期天数（天）
        "billDays": "11",
        # 子账号信息
        "subUserNo": "test-doudian-account-001",
        # 店铺体验分
        "experienceScore": "90",
        # 主要价位（元）
        "price": "90",
        # 客单价（元）
        "customerOrdAmount": "190",
        # 客单量
        "customerOrdCnt30d": "1899",
        # 近3个月实发货额（万元）
        "actualShippedAmount90d": "170",
        # 近一个月后台结算金额（元）
        "ctbAmount30d": "10098",
        # 退货率（%）
        "returnGoodsRate": "30",
        # 当下在途额（万元）
        "transitAmount": "7",
        # 店铺图片
        "storeAttachmentId": [841],
        # 上传原始文件
        "orderAttachmentId": [842]
    }
    response = requests.post(url=url, headers=headers, json=store_data)
    return response.content


def audit_pass(host: str, headers: dict, audit_id: int) -> bytes:
    headers["content-type"] = "application/json"
    url = host + "/fin-portal/controller/audit/audit/pass"
    data = {"isComplete": False, "id": audit_id}
    response = requests.post(url=url, headers=headers, json=data)
    return response.content


if __name__ == "__main__":
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJGSU5fUCIsImlhdCI6MTczODc2MDc1NSwiZXhwIjoxNzM5MzY1NTU1LCJ1c2VyTm8iOiJ3YW5nbWF6aSIsInVzZXJJZCI6IjQifQ.sEPpJt6rwi0HoLJI9WpjIkjgVcpfIm8xWXiZ2pI-v94'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        "Accept-Encoding": "gzip, deflate",
        'Origin': 'http://120.27.128.65:8072',
        'Referer': 'http://120.27.128.65:8072/',
        'Token': token
    }
    # file = '近3个月公司财务报表 (Copy 6).pdf'
    hosts = "http://120.27.128.65:7771"
    # print(upload_attachment(files=file, hosts=hosts, types="7", headers=headers,
    #                         fileType='application/pdf'))
    # print(storeType_config(host=hosts, headers=headers))
    # print(platformType_config(host=hosts, headers=headers))

    # 店铺图片 type: 9 Content-Type: image/jpeg
    # 上传原始文件 type: 10 Content-Type: text/csv

    # 店铺初审
    code = str(uuid.uuid4())
    print(code)
    name = "test-" + str(code)
    print(store_create(host=hosts, headers=headers, code=code, name=name))

    # # 店铺初审 通过
    op = mysql_op(store_ids=code)
    audit_id = op.select_audit_id(status=3)
    print(audit_id)
    print(audit_pass(host=hosts, headers=headers, audit_id=audit_id))

    # # 创建/关联企业
    op = mysql_op(store_ids=code)
    store_id = op.select_store_id()
    print(enterprise_create(host=hosts, headers=headers, store_id=store_id))

    # 卖家终审
    # code = "dc42e5d8-a63c-4dca-8f43-55b6c1d04bbb"
    time.sleep(3)
    op = mysql_op(store_ids=code)
    audit_id_int = op.select_audit_id(status=3)
    print(audit_id_int)
    print(audit_pass(host=hosts, headers=headers, audit_id=audit_id_int))




