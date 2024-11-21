import pymysql as mysql


class Store_apply:
    def __init__(self,
                 store_ids: str,  # 店铺 ID
                 apply_code: str,  # SQ-202411071716-XXXX
                 version: str  # version 必须是 今天 YYYYMMDD
                 ):
        self.store_ids = store_ids  # 店铺ID 唯一
        self.apply_code = apply_code  # 进件 code 唯一
        self.version = version
        self.db = mysql.connect(host="rm-bp19bzj5mc526iot2ho.mysql.rds.aliyuncs.com", port=3306, user='xhdigit_dev',
                                password='Xh1016!@#')
        self.cur = self.db.cursor()

    def sql_execute(self, db_name: str = 'fin_portal_pre'):
        try:
            self.cur.execute(
                f"""select id,enterprise_id from `{db_name}`.`crm_store` cs where cs.code = "{self.store_ids}";""")
            store_id, enterprise_id = self.cur.fetchone()
            print(f'store_id={store_id}--enterprise_id={enterprise_id}')
            # 根据 enterprise_id 查询 code（统一信用代码）
            self.cur.execute(f"""
            select code from `{db_name}`.`crm_enterprise` ce where ce.id = {enterprise_id};;
            """)
            enterprise_cert_no = self.cur.fetchone()[0]
            print(f'enterprise_cert_no={enterprise_cert_no}')
            self.cur.execute(f"""
            INSERT INTO `{db_name}`.`crm_apply`
            ( `enterprise_id`, `enterprise_cert_no`, `store_id`, `code`, `credit_amount`, `loan_amount`, `billing_method`, `cust_rate`, `latest_shipped_date`, `status`, `apply_date`, `payment_date`, `version`, `financing_term`, `applicant`, `loan_operator`, `audit_status`, `is_deleted`, `created`, `updated`)
            VALUES ({enterprise_id}, "{enterprise_cert_no}", {store_id}, "{self.apply_code}", 2117.00, null, 0, 1.000000, '2024-11-06 00:19:02', null, null, null, "{self.version}", 15, null, null, null, 0, now(), now());
            """)
            self.cur.connection.commit()

            self.cur.execute(f'''
            select id from `{db_name}`.`crm_apply` ca
            where ca.enterprise_id = {enterprise_id} and ca.store_id = {store_id};''')
            apply_id= self.cur.fetchone()[0]
            print(f'apply_id={apply_id}')
            # 要插入的数据
            data_to_insert = [
                (apply_id, store_id, '6935827425617057103', '2024-11-03 23:59:37', 1, 99.90, 0.00),
                (apply_id, store_id, '6935936945184707787', '2024-11-06 00:19:02', 1, 114.90, 0.00),
                (apply_id, store_id, '6935923037697217542', '2024-11-05 21:22:45', 1, 129.00, 0.00),
                (apply_id, store_id, '6935916733662631352', '2024-11-05 21:17:51', 1, 129.00, 0.00),
                (apply_id, store_id, '6935868774719166022', '2024-11-04 15:49:31', 1, 99.90, 0.00),
                (apply_id, store_id, '6935849232143488814', '2024-11-03 21:49:14', 1, 129.00, 0.00),
                (apply_id, store_id, '6935838563563935499', '2024-11-03 23:16:40', 1, 129.00, 0.00),
                (apply_id, store_id, '6935829368277833223', '2024-11-03 23:52:43', 1, 99.90, 0.00),
                (apply_id, store_id, '6935828938810136289', '2024-11-03 21:31:16', 1, 129.00, 0.00),
                (apply_id, store_id, '6935686879854204757', '2024-10-31 00:00:51', 1, 99.90, 0.00),
                (apply_id, store_id, '6935804072283346657', '2024-11-03 14:14:58', 1, 129.00, 0.00),
                (apply_id, store_id, '6935705231576405301', '2024-10-31 06:38:23', 1, 139.90, 0.00),
                (apply_id, store_id, '6935700594608051293', '2024-10-31 07:53:54', 1, 139.90, 0.00),
                (apply_id, store_id, '6935699219330897506', '2024-10-31 10:40:00', 1, 129.00, 0.00),
                (apply_id, store_id, '6935698716973339711', '2024-10-31 06:31:25', 1, 139.90, 0.00),
                (apply_id, store_id, '6935698659617674514', '2024-10-31 06:24:55', 1, 139.90, 0.00),
                (apply_id, store_id, '6935687169099175104', '2024-10-31 06:35:50', 1, 139.90, 0.00)
            ]
            sql = f"""
            INSERT INTO `{db_name}`.`crm_apply_order_rel` ( `apply_id`, `store_id`, `order_id`, `shipped_date`, `status`, `estimated_amount`, `settlement_amount`, `settlement_updated`, `created`, `updated`) VALUES ( %s, %s, %s, %s, %s, %s, %s, NULL, now(), now())
            """
            self.cur.executemany(sql, data_to_insert)
            self.cur.connection.commit()

        except mysql.MySQLError as e:
            print(e.args)
            # assert e.args[0] == 1045
        finally:
            self.cur.close()
            self.db.close()
            print("初始化完毕")


if __name__ == '__main__':
    # store_ids: str,  # 店铺 ID
    # apply_code: str,  # SQ-202411071716-XXXX
    # version: str  # version 必须是 今天 YYYYMMDD
    import time
    from datetime import datetime
    # 假设我们有一个time.time()格式的时间戳
    timestamp = time.time()
    # 将时间戳转换为datetime对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 将datetime对象格式化为日期字符串
    version = dt_object.strftime('%Y%m%d')
    apply_code = 'SQ-' + dt_object.strftime('%Y%m%d%H%M-%S')+'00'
    print(f'{apply_code}---{version}')
    p1 = Store_apply(store_ids="asdpoas01", apply_code=apply_code, version=version)
    p1.sql_execute(db_name='fin_portal')
