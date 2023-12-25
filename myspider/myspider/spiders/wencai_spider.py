import copy
import json
import logging
import re

import scrapy
from datetime import datetime, timedelta
import sys

sys.path.append('/Users/mac/python_project/gp_crawler/myspider/myspider/')

from myspider.repo.common_repo import CommonRepo


class MySpider(scrapy.Spider):
    name = 'wencai_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,  # 设置 CONCURRENT_REQUESTS 为 1
        'DOWNLOAD_DELAY': 4,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED': False,

    }
    start_urls = ['https://www.iwencai.com/gateway/urp/v7/landing/getDataList']

    payload = 'source=Ths_iwencai_Xuangu&perpage=100&page=1&urp_sort_way=desc&query=2023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC&condition=%5B%7B%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22score%22%3A0.0%2C%22chunkedResult%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22opName%22%3A%22and%22%2C%22opProperty%22%3A%22%22%2C%22ci%22%3Afalse%2C%22uiText%22%3A%22%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E8%A1%8C%E4%B8%9A%E7%BA%A7%E5%88%AB%E5%8C%85%E5%90%AB%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E6%88%96%E8%80%85%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E5%B9%B6%E4%B8%942023-12-11%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%E5%B9%B6%E4%B8%942023-12-11%E7%9A%84%E6%94%B6%E7%9B%98%E4%BB%B7%22%2C%22sonSize%22%3A6%2C%22opPropertyMap%22%3A%7B%7D%2C%22logid%22%3A%22006e5c681c8ff911bbb856a341935a99%22%2C%22source%22%3A%22text2sql%22%2C%22order%22%3A0%7D%2C%7B%22parentOpName%22%3A%22and%22%2C%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22opName%22%3A%22or%22%2C%22opProperty%22%3A%22%22%2C%22ci%22%3Afalse%2C%22uiText%22%3A%22%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E8%A1%8C%E4%B8%9A%E7%BA%A7%E5%88%AB%E5%8C%85%E5%90%AB%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E6%88%96%E8%80%85%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%2C%22sonSize%22%3A2%2C%22opPropertyMap%22%3A%7B%7D%2C%22parentOpOrder%22%3A0%2C%22order%22%3A1%7D%2C%7B%22dateText%22%3A%22%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E8%A1%8C%E4%B8%9A%E7%BA%A7%E5%88%AB%22%2C%22indexProperties%22%3A%5B%22%E5%8C%85%E5%90%AB%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%5D%2C%22ci%22%3Afalse%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E5%8C%85%E5%90%AB%22%3A%22%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%7D%2C%22parentOpName%22%3A%22or%22%2C%22reportType%22%3A%22null%22%2C%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22uiText%22%3A%22%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E8%A1%8C%E4%B8%9A%E7%BA%A7%E5%88%AB%E5%8C%85%E5%90%AB%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%2C%22valueType%22%3A%22_%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E8%A1%8C%E4%B8%9A%E7%BA%A7%E5%88%AB%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A1%2C%22order%22%3A2%7D%2C%7B%22dateText%22%3A%22%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%22%2C%22indexProperties%22%3A%5B%22EQUAL%20%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%5D%2C%22ci%22%3Afalse%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22EQUAL%22%3A%22%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%7D%2C%22parentOpName%22%3A%22or%22%2C%22reportType%22%3A%22null%22%2C%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22uiText%22%3A%22%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A1%2C%22order%22%3A3%7D%2C%7B%22parentOpName%22%3A%22and%22%2C%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22opName%22%3A%22sort%22%2C%22opProperty%22%3A%22%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%22%2C%22ci%22%3Afalse%2C%22uiText%22%3A%222023-12-11%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%22%2C%22sonSize%22%3A1%2C%22opPropertyMap%22%3A%7B%22%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%22%3A%22%22%7D%2C%22parentOpOrder%22%3A0%2C%22order%22%3A4%7D%2C%7B%22dateText%22%3A%222023-12-11%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E6%B6%A8%E8%B7%8C%E5%B9%85%3A%E5%89%8D%E5%A4%8D%E6%9D%83%22%2C%22indexProperties%22%3A%5B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231211%22%5D%2C%22ci%22%3Afalse%2C%22dateUnit%22%3A%22%E6%97%A5%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231211%22%7D%2C%22parentOpName%22%3A%22sort%22%2C%22reportType%22%3A%22TRADE_DAILY%22%2C%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22dateType%22%3A%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%2C%22isExtend%22%3Afalse%2C%22uiText%22%3A%222023-12-11%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%22%2C%22valueType%22%3A%22_%E6%B5%AE%E7%82%B9%E5%9E%8B%E6%95%B0%E5%80%BC(%25)%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A4%2C%22order%22%3A5%7D%2C%7B%22dateText%22%3A%222023-12-11%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E6%94%B6%E7%9B%98%E4%BB%B7%3A%E4%B8%8D%E5%A4%8D%E6%9D%83%22%2C%22indexProperties%22%3A%5B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231211%22%5D%2C%22ci%22%3Afalse%2C%22dateUnit%22%3A%22%E6%97%A5%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231211%22%7D%2C%22parentOpName%22%3A%22and%22%2C%22reportType%22%3A%22TRADE_DAILY%22%2C%22ciChunk%22%3A%222023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22dateType%22%3A%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%2C%22isExtend%22%3Afalse%2C%22uiText%22%3A%222023-12-11%E7%9A%84%E6%94%B6%E7%9B%98%E4%BB%B7%22%2C%22valueType%22%3A%22_%E6%B5%AE%E7%82%B9%E5%9E%8B%E6%95%B0%E5%80%BC(%E5%85%83%7C%E6%B8%AF%E5%85%83%7C%E7%BE%8E%E5%85%83%7C%E8%8B%B1%E9%95%91)%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A0%2C%22order%22%3A6%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%40%E6%B6%A8%E8%B7%8C%E5%B9%85%3A%E5%89%8D%E5%A4%8D%E6%9D%83%5B20231211%5D&codelist=&page_id=&logid=006e5c681c8ff911bbb856a341935a99&ret=json_all&sessionid=006e5c681c8ff911bbb856a341935a99&iwc_token=&user_id=Ths_iwencai_Xuangu_kbcw76etxhl0ulv3td9qxunz99a3roxo&uuids%5B0%5D=24089&query_type=zhishu&comp_id=6829723&business_cat=soniu&uuid=24089'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'other_uid=Ths_iwencai_Xuangu_kbcw76etxhl0ulv3td9qxunz99a3roxo; ta_random_userid=ossduam4se; cid=a2fd6ebdfa53807c0741b38108b4a9651702001061; THSSESSID=e732cd299797d702fef15def45; v=AyZl1JL3f8Pk6ituhnh_Ybstd5etB2ABPG2eRBClFswlEcgJeJe60Qzb7lLj',
        'Origin': 'https://www.iwencai.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.iwencai.com/unifiedwap/result?w=2023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC&querytype=zhishu',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'hexin-v': 'AyZl1JL3f8Pk6ituhnh_Ybstd5etB2ABPG2eRBClFswlEcgJeJe60Qzb7lLj',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    payload_sz = 'source=Ths_iwencai_Xuangu&perpage=100&page=1&urp_sort_way=desc&query=2023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC&condition=%5B%7B%22ciChunk%22%3A%222023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22score%22%3A0.0%2C%22chunkedResult%22%3A%222023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22opName%22%3A%22and%22%2C%22opProperty%22%3A%22%22%2C%22ci%22%3Afalse%2C%22uiText%22%3A%22%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E5%B9%B6%E4%B8%942023-12-11%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%E5%B9%B6%E4%B8%942023-12-11%E7%9A%84%E6%94%B6%E7%9B%98%E4%BB%B7%22%2C%22sonSize%22%3A4%2C%22opPropertyMap%22%3A%7B%7D%2C%22logid%22%3A%22ef0fb43a862057eb28e5144459d6c274%22%2C%22source%22%3A%22text2sql%22%2C%22order%22%3A0%7D%2C%7B%22dateText%22%3A%22%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%22%2C%22indexProperties%22%3A%5B%22EQUAL%20%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%5D%2C%22ci%22%3Afalse%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22EQUAL%22%3A%22%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%7D%2C%22parentOpName%22%3A%22and%22%2C%22reportType%22%3A%22null%22%2C%22ciChunk%22%3A%222023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22uiText%22%3A%22%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%AE%80%E7%A7%B0%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A0%2C%22order%22%3A1%7D%2C%7B%22parentOpName%22%3A%22and%22%2C%22ciChunk%22%3A%222023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22opName%22%3A%22sort%22%2C%22opProperty%22%3A%22%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%22%2C%22ci%22%3Afalse%2C%22uiText%22%3A%222023-12-11%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%22%2C%22sonSize%22%3A1%2C%22opPropertyMap%22%3A%7B%22%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%22%3A%22%22%7D%2C%22parentOpOrder%22%3A0%2C%22order%22%3A2%7D%2C%7B%22dateText%22%3A%222023-12-11%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E6%B6%A8%E8%B7%8C%E5%B9%85%3A%E5%89%8D%E5%A4%8D%E6%9D%83%22%2C%22indexProperties%22%3A%5B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231211%22%5D%2C%22ci%22%3Afalse%2C%22dateUnit%22%3A%22%E6%97%A5%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231211%22%7D%2C%22parentOpName%22%3A%22sort%22%2C%22reportType%22%3A%22TRADE_DAILY%22%2C%22ciChunk%22%3A%222023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22dateType%22%3A%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%2C%22isExtend%22%3Afalse%2C%22uiText%22%3A%222023-12-11%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%22%2C%22valueType%22%3A%22_%E6%B5%AE%E7%82%B9%E5%9E%8B%E6%95%B0%E5%80%BC(%25)%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A2%2C%22order%22%3A3%7D%2C%7B%22dateText%22%3A%222023-12-11%22%2C%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E6%94%B6%E7%9B%98%E4%BB%B7%3A%E4%B8%8D%E5%A4%8D%E6%9D%83%22%2C%22indexProperties%22%3A%5B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231211%22%5D%2C%22ci%22%3Afalse%2C%22dateUnit%22%3A%22%E6%97%A5%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231211%22%7D%2C%22parentOpName%22%3A%22and%22%2C%22reportType%22%3A%22TRADE_DAILY%22%2C%22ciChunk%22%3A%222023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC%22%2C%22dateType%22%3A%22%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%2C%22isExtend%22%3Afalse%2C%22uiText%22%3A%222023-12-11%E7%9A%84%E6%94%B6%E7%9B%98%E4%BB%B7%22%2C%22valueType%22%3A%22_%E6%B5%AE%E7%82%B9%E5%9E%8B%E6%95%B0%E5%80%BC(%E5%85%83%7C%E6%B8%AF%E5%85%83%7C%E7%BE%8E%E5%85%83%7C%E8%8B%B1%E9%95%91)%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22sonSize%22%3A0%2C%22parentOpOrder%22%3A0%2C%22order%22%3A4%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%40%E6%B6%A8%E8%B7%8C%E5%B9%85%3A%E5%89%8D%E5%A4%8D%E6%9D%83%5B20231211%5D&codelist=&page_id=&logid=ef0fb43a862057eb28e5144459d6c274&ret=json_all&sessionid=ef0fb43a862057eb28e5144459d6c274&iwc_token=&user_id=Ths_iwencai_Xuangu_kbcw76etxhl0ulv3td9qxunz99a3roxo&uuids%5B0%5D=24089&query_type=zhishu&comp_id=6829723&business_cat=soniu&uuid=24089'
    headers_sz = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'other_uid=Ths_iwencai_Xuangu_kbcw76etxhl0ulv3td9qxunz99a3roxo; ta_random_userid=ossduam4se; cid=a2fd6ebdfa53807c0741b38108b4a9651702001061; THSSESSID=e732cd299797d702fef15def45; v=AxlabSnWmPfUwkRjEXo4KMDcKA72pg8795kx7DvKlE6_ajdwg_YdKIfqQabI',
        'Origin': 'https://www.iwencai.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.iwencai.com/unifiedwap/result?w=2023-12-11%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC&querytype=zhishu',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'hexin-v': 'AxlabSnWmPfUwkRjEXo4KMDcKA72pg8795kx7DvKlE6_ajdwg_YdKIfqQabI',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }


    # 2023-12-11的二级行业板块或上证指数的涨跌幅排行与价格
    # https://www.iwencai.com/unifiedwap/result?w=2023-12-11%E7%9A%84%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E6%9D%BF%E5%9D%97%E6%88%96%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%E7%9A%84%E6%B6%A8%E8%B7%8C%E5%B9%85%E6%8E%92%E8%A1%8C%E4%B8%8E%E4%BB%B7%E6%A0%BC&querytype=zhishu
    commonRepo = CommonRepo()
    def start_requests(self):
        start_date = datetime(2023, 12, 6)  # 指定年、月、日
        current_date = start_date
        end_date =  datetime(2023, 12, 24)

        while current_date <= end_date:
            print(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

            payload, date = self.assem_payload(current_date)
            yield scrapy.Request(
                url=self.start_urls[0],
                method='POST',
                headers=self.headers,
                body=json.dumps(payload),
                callback=self.parse,
                meta={"date": date}
            )

            payload_sz, date = self.assem_payload_sz(current_date)
            yield scrapy.Request(
                url=self.start_urls[0],
                method='POST',
                headers=self.headers_sz,
                body=json.dumps(payload_sz),
                callback=self.parse,
                meta={"date": date}
            )

    def assem_payload(self, date):
        date1 = date.strftime("%Y-%m-%d")
        date2 = date.strftime("%Y%m%d")
        payload = copy.copy(self.payload)
        payload = payload.replace("2023-12-11", date1)
        payload = payload.replace("20231211", date2)
        return payload, date2

    def assem_payload_sz(self, date):
        date1 = date.strftime("%Y-%m-%d")
        date2 = date.strftime("%Y%m%d")
        payload = copy.copy(self.payload_sz)
        payload = payload.replace("2023-12-11", date1)
        payload = payload.replace("20231211", date2)
        return payload, date2

    def parse(self, response):
        meta = response.request.meta
        # date = meta['date']
        if response.status != 200:
            logging.error("状态码错误")
            return

        res = json.loads(response.text)
        if "status_code" not in res:
            logging.error(f"res异常 {res}")
            return
        if res['status_code'] != "0":
            logging.error(f"res code 异常 {res}")
            # 如果当前页面请求失败的话
            return
        datas = res['answer']['components'][0]['data']['datas']
        date = 0
        for row in datas:
            if date:
                break
            for key, value in reversed(list(row.items())):

                match = re.search(r"\[(\d{8})\]", key)
                if match:
                    date = match.group(1)
                    break
        if date:
            for row in datas:
                fluctuation_range = row[f"指数@涨跌幅:前复权[{date}]"]
                closing_price = row[f"指数@收盘价:不复权[{date}]"]
                name = row["指数简称"]
                try:
                    self.commonRepo.save_industry_daily_data({"fluctuation_range": fluctuation_range, "name": name, "date":date, "closing_price":closing_price})
                except Exception as e:
                    logging.error(e)






