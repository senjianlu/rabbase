#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rabbir/rabbase/proxy.py
# @DATE: 2022/08/19 周五
# @TIME: 19:41:30
#
# @DESCRIPTION: 代理模块


import rab_orm


class Proxy(rab_orm.BaseClass):
    """
    代理类
    """

    def __init__(self, protocol, ip, port, username, password):
        """
        初始化
        """
        super(Proxy, self).__init__("rabbase_proxy", ["id"])
        self.protocol = protocol
        self.ip = ip
        # 备用 host 字段，有的代理可能使用域名解析
        self.host = None
        self.port = port
        self.username = username
        self.password = password
        self.out_ip = None
        self.out_country_code = None
        self.out_country_name = None
        self.out_country_name_zh = None
        self.node_id = None
