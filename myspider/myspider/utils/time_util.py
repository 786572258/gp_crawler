import logging
import re
from datetime import datetime

def strCoverToTimestamp(time_string, is_ms=False):
    """
    格式化时间转时间戳
    支持时间格式："2016-11-29" 或 "2016-11-29 14:30:45"
    """
    # 定义日期和时间的正则表达式模式
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    datetime_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"

    # 使用正则表达式进行校验
    if re.match(datetime_pattern, time_string):
        format_string = "%Y-%m-%d %H:%M:%S"
    elif re.match(date_pattern, time_string):
        format_string = "%Y-%m-%d"
    else:
        logging.error("时间字符串格式不正确")
        return 0

    try:
        # 尝试使用正确的格式解析时间字符串
        date_obj = datetime.strptime(time_string, format_string)

        # 将 datetime 对象转换为毫秒级时间戳
        if is_ms:
            timestamp = int(date_obj.timestamp() * 1000)
        else:
            timestamp = int(date_obj.timestamp())

        return timestamp
    except ValueError:
        logging.error("时间字符串无法解析")
        return 0





