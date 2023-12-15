import redis

from ycgYangguan.utils.config import spiderConfig

redis_conn = None

# 多线程下暂时不知道会不会有问题
def redis_connect():
    global redis_conn
    if redis_conn is not None:
        return redis_conn

    # 建立连接
    try:
        redis_conn = redis.Redis(host=spiderConfig["Redis"]["host"], port=spiderConfig["Redis"]["port"],
                                 password=spiderConfig["Redis"]["password"])
    except Exception as e:
        raise f"无法连接到 Redis 服务器。{e}"
    return redis_conn

    # 使用例子
    # print(redis_conn)
    # redis_conn.set('mykey', 'Hello, Redis!', ex=90)
    # value_cache = redis_conn.get("mykey")
    # print(value_cache.decode('utf-8'))  # 解码为字符串
