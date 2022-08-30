#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/Projects/rabbir/rabbase/node.py
# @DATE: 2022/08/19 周五
# @TIME: 20:40:14
#
# @DESCRIPTION: 节点模块


import urllib

import rab_orm
import rab_decoder


# 代理种类
KINDS = ["vps", "vpn", "sub"]
# 代理种类
PROTOCOLS = ["pptp", "ipsec", "ikev2", "l2tp", "sstp", "openvpn", "wireguard",
             "ss", "ssr", "vmess", "trojan", "vless"]


def parse_ss_node(node_origin_info):
    """
    解析 SS 协议的节点
    """
    node_info = {}
    node_info["type"] = "ss"
    node = node_origin_info.replace("ss://", "", 1)
    node_info["name"] = urllib.parse.unquote(
        node.split("@")[1].split("#")[1]).rstrip("\n")
    node_info["server"] = node.split("@")[1].split("#")[0].split(":")[0]
    node_info["port"] = node.split("@")[1].split("#")[0].split(":")[1]
    # 部分 Base64 解码
    part_node = node.replace("ss://", "", 1).split("@")[1]
    part_node = rab_decoder.b64decode(part_node).decode("UTF-8")
    node_info["cipher"] = part_node.split(":")[0]
    node_info["password"] = part_node.split(":")[1]
    return node_info


def parse_ssr_node(node_origin_info):
    """
    解析 SSR 协议的节点
    """
    node_info = {}
    node_info["type"] = "ssr"
    node = node_origin_info.replace("ssr://", "", 1)
    # Base64 解码
    node = rab_decoder.b64decode_mix(node).decode("UTF-8")
    node_params = urllib.parse.parse_qs(
        urllib.parse.urlparse("/?"+node.split("/?")[1]).query)
    print(node, node_params)
    node_info["name"] = rab_decoder.b64decode_mix(
        node_params["remarks"][0]).decode("UTF-8")
    node_info["server"] = node.split("/?")[0].split(":")[0]
    node_info["port"] = node.split("/?")[0].split(":")[1]
    node_info["protocol"] = node.split("/?")[0].split(":")[2]
    node_info["cipher"] = node.split("/?")[0].split(":")[3]
    node_info["obfs"] = node.split("/?")[0].split(":")[4]
    node_info["password"] = rab_decoder.b64decode_mix(
        node.split("/?")[0].split(":")[5]).decode("UTF-8")
    node_info["protocol-param"] = rab_decoder.b64decode_mix(
        node_params["protoparam"][0]).decode("UTF-8")
    if ("node_params" in node_params):
        node_info["obfs-param"] = rab_decoder.b64decode_mix(
            node_params["obfsparam"][0]).decode("UTF-8")
    return node_info


class Node(rab_orm.BaseClass):
    """
    代理类
    """

    def __init__(self,
                 kind,
                 origin_info,
                 subscription_id):
        """
        初始化
        """
        super(Node, self).__init__("rabbase_node", ["id"])
        self.kind = kind
        self.protocol = None
        # 节点原始信息：VPN 协议为文件内容，机场订阅为 Base64 解码前的节点信息
        self.origin_info = origin_info
        # 节点信息
        self.info = None
        # 所属订阅组
        self.subscription_id = subscription_id
        # 订阅所在服务器 ID
        self.server_id = None
        # 订阅所在的容器 ID
        self.container_id = None
        # 是否已经转变为代理
        self.is_become_proxy = 0
    
    def parse(self, extra_node_info: dict = {}):
        """
        解析节点
        """
        node_info = {}
        node_info.update(extra_node_info)
        if (self.kind == "sub"):
            if (self.origin_info.startswith("ss://")):
                self.protocol = "ss"
                node_info = parse_ss_node(self.origin_info)
            elif (self.origin_info.startswith("ssr://")):
                self.protocol = "ssr"
                node_info = parse_ssr_node(self.origin_info)
            else:
                raise Exception(
                    f"暂不支持该协议的代理节点解析！节点原始信息：{self.origin_info}")
        elif (self.kind == "vpn"):
            node_info["ovpn_file_content"] = self.origin_info
        self.info = node_info