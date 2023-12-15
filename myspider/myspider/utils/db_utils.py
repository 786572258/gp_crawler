import pymysql

def db_connect():
    mysql_conn = pymysql.connect(
        host=spiderConfig['Mysql']['host'], port=spiderConfig['Mysql']['port'],
        user=spiderConfig['Mysql']['username'], password=spiderConfig['Mysql']['password'],
        database=spiderConfig['Mysql']['database'], charset=spiderConfig['Mysql']['charset'],
        cursorclass=pymysql.cursors.DictCursor, autocommit=True,
    )
    return mysql_conn


def db_connect_crawler():
    mysql_conn = pymysql.connect(
        host=spiderConfig['MysqlCrawler']['host'], port=spiderConfig['MysqlCrawler']['port'],
        user=spiderConfig['MysqlCrawler']['username'], password=spiderConfig['MysqlCrawler']['password'],
        database=spiderConfig['MysqlCrawler']['database'], charset=spiderConfig['MysqlCrawler']['charset'],
        autocommit=True, cursorclass=pymysql.cursors.DictCursor
    )
    return mysql_conn


def db_connect_data_center():
    mysql_conn = pymysql.connect(
        host=spiderConfig['MysqlDataCenter']['host'], port=spiderConfig['MysqlDataCenter']['port'],
        user=spiderConfig['MysqlDataCenter']['username'], password=spiderConfig['MysqlDataCenter']['password'],
        database=spiderConfig['MysqlDataCenter']['database'], charset=spiderConfig['MysqlDataCenter']['charset'],
        autocommit=True, cursorclass=pymysql.cursors.DictCursor
    )
    return mysql_conn


def db_connect_bid_data():
    mysql_conn = pymysql.connect(
        host=spiderConfig['MysqlBidData']['host'], port=spiderConfig['MysqlBidData']['port'],
        user=spiderConfig['MysqlBidData']['username'], password=spiderConfig['MysqlBidData']['password'],
        database=spiderConfig['MysqlBidData']['database'], charset=spiderConfig['MysqlBidData']['charset'],
        autocommit=True, cursorclass=pymysql.cursors.DictCursor
    )
    return mysql_conn


# 批量插入 to_db_dict_list是有序字典数组
def batch_insert(cursor, table_name, to_db_dict_list):
    fields = ', '.join([f"`{key}`" for key in to_db_dict_list[0].keys()])
    placeholders = ', '.join(['%s'] * len(to_db_dict_list[0]))
    insert_sql = f"INSERT INTO `{table_name}` ({fields}) VALUES ({placeholders})"

    # 提取字典列表中的值并构建插入数据的元组
    values = [tuple(item.values()) for item in to_db_dict_list]

    # 执行批量插入操作
    rs = cursor.executemany(insert_sql, values)
    return rs


# 删除
def delete(cursor, table_name, where_parmas):
    query_conditions = where_parmas[0]
    query_params = where_parmas[1:]
    sql = f"delete from {table_name} where {query_conditions}"
    rs = cursor.execute(sql, query_params)
    return rs


# 删除
def insert(cursor, table_name, to_db_dict):
    db_fields = list(to_db_dict.keys())
    # 使用反引号 `` 包裹字段名
    quoted_fields = [f"`{field}`" for field in db_fields]
    placeholders = ','.join(['%s'] * len(db_fields))
    fields_str = ','.join(quoted_fields)  # 使用带有反引号的字段名
    sql_exec = f'insert into {table_name} ({fields_str}) values({placeholders})'
    values_arr = list(to_db_dict.values())
    rs = cursor.execute(sql_exec, values_arr)
    return rs


def insert_replace(cursor, table_name, to_db_dict):
    db_fields = list(to_db_dict.keys())
    quoted_fields = [f"`{field}`" for field in db_fields]
    placeholders = ','.join(['%s'] * len(db_fields))
    fields_str = ','.join(quoted_fields)

    # 构造 UPDATE 子句
    update_clause = ','.join([f"`{field}`=%s" for field in db_fields])

    # 构造 SQL 语句
    sql_exec = f'INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders}) ' \
               f'ON DUPLICATE KEY UPDATE {update_clause}'

    values_arr = list(to_db_dict.values()) * 2  # 在执行语句时需要两次相同的值
    rs = cursor.execute(sql_exec, values_arr)
    return rs



def update(cursor, table_name, to_db_dict, where_parmas):
    query_conditions = where_parmas[0]
    query_params = where_parmas[1:]
    # 构建 SET 子句
    set_clause = ', '.join([f"`{field}` = %s" for field in to_db_dict.keys()])
    # 构建 UPDATE SQL 语句
    sql_exec = f'UPDATE {table_name} SET {set_clause} WHERE {query_conditions}'
    # 执行 SQL 语句
    rs = cursor.execute(sql_exec, list(to_db_dict.values()) + list(query_params))
    return rs


# 获取一条
def first(cursor, table_name, where_parmas, field="*", order_by=""):
    query_conditions = where_parmas[0]
    query_params = where_parmas[1:]
    # 构建 SET 子句
    # 构建 UPDATE SQL 语句
    sql_exec = f'select {field} from {table_name} WHERE {query_conditions}'
    if order_by:
        sql_exec = sql_exec + f" order by {order_by}"
    sql_exec = sql_exec
    # 执行 SQL 语句
    cursor.execute(sql_exec, query_params)
    return cursor.fetchone()


# 获取多条
def find(cursor, table_name, where_parmas, limit, field="*", order_by=""):
    query_conditions = where_parmas[0]
    query_params = where_parmas[1:]
    # 构建 SET 子句
    # 构建 UPDATE SQL 语句
    sql_exec = f'select {field} from {table_name} WHERE {query_conditions}'
    if order_by:
        sql_exec = sql_exec + f" order by {order_by}"
    sql_exec = sql_exec + f" limit {limit}"
    # 执行 SQL 语句
    print(sql_exec)
    cursor.execute(sql_exec, query_params)
    return cursor.fetchall()


# 获取count
def count(cursor, table_name, where_parmas):
    query_conditions = where_parmas[0]
    query_params = where_parmas[1:]
    # 构建 SET 子句
    # 构建 UPDATE SQL 语句
    sql_exec = f'select count(1) as c from {table_name} WHERE {query_conditions}'
    # 执行 SQL 语句
    cursor.execute(sql_exec, query_params)
    return cursor.fetchone()['c']
