#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rabbir/rabbase/subscription.py
# @DATE: 2022/08/20 周六
# @TIME: 15:51:17
#
# @DESCRIPTION: 订阅模块


import os
import shutil
import zipfile
import requests
from requests.adapters import HTTPAdapter

import rab_orm
import rab_decoder


# 订阅种类
KINDS = ["vpn", "sub"]
# 流量使用模式
TRAFFIC_MODE = ["unlimited", "payg", "periodic"]
# 连接超时秒数
CONNECT_TIMEOUT = 5
# 读取超时秒数
READ_TIMEOUT = 30
# 失败重试次数（总次数 + 1）
MAX_RETRIES = 3
# 临时用的 VPN 节点文件压缩包名
TEMP_VPN_NODES_ZIP = "temp/vpn_nodes.zip"
# 临时用的 VPN 节点文件压缩包名
TEMP_VPN_NODES_DIR = "temp/vpn_nodes"


class Subscription(rab_orm.BaseClass):
    """
    订阅类
    """

    def __init__(self, kind, url):
        """
        初始化
        """
        super(Subscription, self).__init__("rabbase_subscription", ["id"])
        self.kind = kind
        self.url = url
        # 是否已经请求
        self.is_request = 0
        # 原始的请求信息
        self.response_content = None
        # 是否已经解析
        self.is_parse = 0
        # 节点数量
        self.nodes_count = None
        # 节点原始信息列表
        self.node_origin_infos = []
        # 节点 ID 列表（PostgreSQL 支持列表格式数据的存取）
        self.node_ids = []
        # 节点认证信息
        self.node_auth_info = None
        # 流量使用模式
        self.traffic_mode = None
        # 流量限制（单位为 mb）
        self.traffic_maximum = None
        # 流量已使用（单位为 mb）
        self.traffic_used = None
        # 流量下次重置日期
        self.traffic_next_reset_date = None
        # 订阅过期日期
        self.expiration_date = None
        # 订阅提供商名字
        self.provider_name = None
        # 订单提供商地址
        self.provider_url = None
        # 订阅提供商登陆用户名
        self.provider_auth_username = None
        # 订阅提供商登陆用户名
        self.provider_auth_password = None

    def request(self):
        """
        请求订阅地址获取原始信息
        """
        # 请求原始信息
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=5))
        session.mount('https://', HTTPAdapter(max_retries=5))
        response = session.get(
            self.url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        # 请求成功则保存信息
        if (response.status_code == 200):
            self.is_request = True
            self.response_content = response.content

    def parse(self):
        """
        解析出节点的原始信息

        使用 subconverter 容器建立服务实现。
        """
        # 机场订阅
        if (self.kind == "sub"):
            # Base64 解码后分割
            decoded_response_content = rab_decoder.b64decode_mix(
                self.response_content.decode("UTF-8")).decode("UTF-8")
            for origin_node_info in decoded_response_content.split("\n"):
                if (origin_node_info.strip()):
                    self.node_origin_infos.append(origin_node_info)
        # VPN 协议
        elif (self.kind == "vpn"):
            # 写入压缩包后解压
            with open(TEMP_VPN_NODES_ZIP, "wb") as zip_file:
                zip_file.write(self.response_content)
            _zipfile = zipfile.ZipFile(
                TEMP_VPN_NODES_ZIP, "r", zipfile.ZIP_DEFLATED)
            _zipfile.extractall(TEMP_VPN_NODES_DIR)
            # 读取各节点文件内容
            for path, dir_names, file_names in os.walk(TEMP_VPN_NODES_DIR):
                for file_name in file_names:
                    file_path = os.path.join(path, file_name)
                    with open(file_path, "r") as file:
                        self.node_origin_infos.append(file.read())
            # 删除临时压缩包和文件夹
            os.remove(TEMP_VPN_NODES_ZIP)
            shutil.rmtree(TEMP_VPN_NODES_DIR)
        # 节点数
        self.nodes_count = len(self.node_origin_infos)
        # print(self.nodes_count)


# 临时测试
if __name__ == "__main__":
    # VPN 订阅
    test_subscription = Subscription(
        "vpn", "https://my.surfshark.com/vpn/api/v1/server/configurations")
    test_subscription.node_auth_info = {
        "username": "112233",
        "password": "445566"
    }
    test_subscription.request()
    test_subscription.parse()
    # 解析节点
    import rab_node
    for node_origin_info in test_subscription.node_origin_infos:
        _node = rab_node.Node("vpn", node_origin_info, "test")
        _node.parse(test_subscription.node_auth_info)
        print(_node.info)