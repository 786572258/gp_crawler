import logging
import re
import secrets
import string
import time
import uuid

import requests


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# 判断是否是数字
def is_number(value):
    if re.match(r'^[0-9]+$', value):
        return True
    else:
        return False

# 生成uuid
def gen_uuid():
    return f"{uuid.uuid4()}"

# 同步请求
def send_request(url, method, headers=None, body=None):
    err = None
    for _ in range(2):
        try:
            if method == 'POST':
                response = requests.post(url, headers=headers, data=body, timeout=40)
            else:
                response = requests.get(url, headers=headers, timeout=40)
            response.close()

            return response
        except Exception as e:
            err = e
            logging.warning("send_request An error occurred:", e)
            logging.warning("send_request Retrying...")
            time.sleep(1)  # 可以添加延迟，避免过于频繁的重试

    if err:
        raise err
    return None  # 重试多次后仍然失败，返回 None 或适当的响应


# scrapy请求重试 self为spider对象，response为scrapy response对象
def request_replace(self, response):
    # 重试
    retry_times = response.request.meta.get('retry_times', 0)
    if retry_times >= self.custom_settings['RETRY_TIMES']:
        return
    meta = response.request.meta
    meta["retry_times"] = retry_times + 1
    logging.warning(f"第{meta['retry_times']}次重试...")
    if self.custom_settings.get('RETRY_DELAY'):
        time.sleep(self.custom_settings.get('RETRY_DELAY'))

    return response.request.replace(dont_filter=True, meta=meta)  # 显式重试请求 dont_filter 表示绕过Scrapy默认的请求去重机制