#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rabbir/rabbase/ip.py
# @DATE: 2022/08/19 周五
# @TIME: 17:30:06
#
# @DESCRIPTION: IP 鉴别


import json
import requests


# 超时秒数
TIMEOUT = 3


def get_info(proxies: dict) -> dict:
    """
    获取 IP 信息
    """
    info = {
        "ip": None,
        "location": {
            "country_code": None,
            "country_name": None,
            "country_name_zh": None,
        }
    }
    # 接口提供：myip.la
    if (not info["ip"]):
        try:
            response = requests.get("https://api.myip.la/en?json",
                                    proxies=proxies,
                                    timeout=TIMEOUT)
            origin_info = json.loads(response.text)
            info["ip"] = origin_info["ip"]
            info["location"]["country_code"] = origin_info["location"][
                "country_code"]
            info["location"]["country_name"] = origin_info["location"][
                "country_name"]
        except Exception:
            pass
    # 接口提供：ip-api.io
    if (not info["ip"]):
        try:
            response = requests.get("https://ip-api.io/json",
                                    proxies=proxies,
                                    timeout=TIMEOUT)
            origin_info = json.loads(response.text)
            info["ip"] = origin_info["ip"]
            info["location"]["country_code"] = origin_info["country_code"]
            info["location"]["country_name"] = origin_info["country_name"]
        except Exception:
            pass
    # 接口提供：ipwho.is
    if (not info["ip"]):
        try:
            response = requests.get("http://ipwho.is",
                                    proxies=proxies,
                                    timeout=TIMEOUT)
            origin_info = json.loads(response.text)
            info["ip"] = origin_info["ip"]
            info["location"]["country_code"] = origin_info["country_code"]
            info["location"]["country_name"] = origin_info["country"]
        except Exception:
            pass
    # 接口提供：ip-api.com
    if (not info["ip"]):
        try:
            response = requests.get("http://ip-api.com/json/?lang=zh-EN",
                                    proxies=proxies,
                                    timeout=TIMEOUT)
            origin_info = json.loads(response.text)
            info["ip"] = origin_info["query"]
            info["location"]["country_code"] = origin_info["countryCode"]
            info["location"]["country_name"] = origin_info["country"]
        except Exception:
            pass
    return info


# 临时测试
if __name__ == "__main__":
    local_proxies = {
        "http": "socks5://127.0.0.1:47893",
        "https": "socks5://127.0.0.1:47893"
    }
    print("当前使用的代理信息：", get_info(local_proxies))
