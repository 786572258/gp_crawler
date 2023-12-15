import hashlib
import re


def generate_md5(content):
    hash_object = hashlib.md5()
    # 将字符串编码并传递给 update() 方法
    hash_object.update(content.encode("utf-8"))
    # 获取 MD5 散列值的十六进制表示
    md5_hash = hash_object.hexdigest()
    return md5_hash

def is_english_and_underline(text):
    # 使用正则表达式匹配只包含英文字母和下划线的字符串
    pattern = r'^[a-zA-Z_]+$'
    return bool(re.match(pattern, text))

# 判断是否存在中文
# 测试
# text1 = "Hello, 你好吗？"
# text2 = "This is an English sentence."
# print(contains_chinese(text1))  # 输出 True
# print(contains_chinese(text2))  # 输出 False
def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    return bool(pattern.search(text))

