#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/GitHub/Clash-docker/test/cryptography.py
# @DATE: 2022/08/05 周五
# @TIME: 15:07:57
#
# @DESCRIPTION: 解码模块


import base64


def b64decode(s) -> str:
    """
    Base64 解码
    """
    return base64.b64decode(s + "="*(4-(len(s) % 4)))


def urlsafe_b64decode(s) -> str:
    """
    Url Base64 解码
    """
    return base64.urlsafe_b64decode(s + "="*(4-(len(s) % 4)))


def b64decode_mix(s) -> str:
    """
    Base64 解码混合方法
    """
    if ("-" in s or "_" in s):
        return urlsafe_b64decode(s)
    else:
        return b64decode(s)
