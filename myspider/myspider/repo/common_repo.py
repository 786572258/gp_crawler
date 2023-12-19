from datetime import datetime, timedelta

import pymysql

from myspider.utils import db_utils


class CommonRepo:

    def __init__(self):
        mysql_conn = pymysql.connect(
            host="127.0.0.1", port=3306,
            user='root', password='root',
            database='gp', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        self.cursor = mysql_conn.cursor()

    def save_industry_daily_data(self, data):
        return db_utils.insert_replace(self.cursor, "industry_daily_data", data)

    def find_industry_daily_data(self, days):
        where = "1 = %s"
        where_value = [1]
        if days:
            current_date = datetime.now()
            # 计算10天前的日期
            ten_days_ago = current_date - timedelta(days=int(days))
            # 将日期格式化为字符串
            formatted_date = ten_days_ago.strftime('%Y%m%d')
            where += " and date > %s"
            where_value.append(formatted_date)
        return db_utils.find(self.cursor, "industry_daily_data", (where, *where_value), 99999999)
    #
    # # 获取土地数据
    # def get_land_data_list(self, offset, limit):
    #     select_sql = f"select * from uuc_land_data  where is_deleted = 0 limit {limit} offset {offset} "
    #     self.cursor.execute(select_sql)
    #     result = self.cursor.fetchall()
    #     return result
    #
    # def get_duplicate_land_data_list_by_field(self, project_name, company_name, city, take_land_date, area, info_type):
    #     select_sql = "SELECT * FROM uuc_land_data WHERE project_name = %s and company_name = %s and city=%s and take_land_date = %s and area = %s and info_type = %s and is_deleted = 0 order by source_update_time,updated_time desc limit 100 "
    #     self.cursor.execute(select_sql, (project_name, company_name, city, take_land_date, area, info_type))
    #     result = self.cursor.fetchall()
    #     return result
    #
    # def update_land_datas_by_uids(self, update_data, uids):
    #     result = db_utils.update(self.cursor, "uuc_land_data", update_data, (f"`uid` in %s", uids))
    #     return result