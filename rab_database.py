#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/GitHub/rabbase/database.py
# @DATE: 2022/08/14 周日
# @TIME: 15:33:10
#
# @DESCRIPTION: 数据库连接工具


from typing import Tuple
import pymysql
import psycopg2
import psycopg2.extras


class Driver():
    """
    数据库连接驱动器
    """

    def __init__(self, type_, host, port: int, username, password, database):
        """
        初始化
        """
        self.type_ = type_
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        # 数据库连接和光标
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        建立数据库连接
        """
        # PostgreSQL 数据库
        if (self.type_.lower() == "postgresql"):
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port)
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
        # MySQL 数据库
        elif (self.type_.lower() == "mysql"):
            self.connection = pymysql.connect(
                database=self.database,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port)
            self.cursor = self.connection.cursor(
                cursor=pymysql.cursors.DictCursor)
        else:
            print(f"暂不支持该数据库类型：{self.type_}")

    def execute(self,
                action,
                sql,
                values: list = [],
                filter_values: list = []) -> Tuple[int, list]:
        """
        执行 SQL
        """
        # PostgreSQL 数据库
        if (self.type_.lower() == "postgresql"):
            if (action == "select"):
                self.cursor.execute(sql, filter_values)
                row_count = self.cursor.rowcount
                return row_count, self.cursor.fetchall()
            elif (action == "insert"):
                self.cursor.execute(sql, values)
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
            elif (action == "update"):
                self.cursor.execute(sql, [*values, *filter_values])
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
            elif (action == "delete"):
                self.cursor.execute(sql, filter_values)
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
            else:
                self.cursor.execute(sql, [*values, *filter_values])
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
        # MySQL 数据库
        elif (self.type_.lower() == "mysql"):
            self.connection.commit()
            if (action == "select"):
                self.cursor.execute(sql, filter_values)
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, self.cursor.fetchall()
            elif (action == "insert"):
                self.cursor.execute(sql, values)
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
            elif (action == "update"):
                self.cursor.execute(sql, [*values, *filter_values])
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
            elif (action == "delete"):
                self.cursor.execute(sql, filter_values)
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
            else:
                self.cursor.execute(sql, [*values, *filter_values])
                row_count = self.cursor.rowcount
                self.connection.commit()
                return row_count, []
        else:
            print(f"暂不支持该数据库类型：{self.type_}")

    def test(self):
        """
        测试连接
        """
        test_sql = "SELECT 1;"
        return self.execute("select", test_sql)

    def select(self, sql, filter_values):
        """
        检索
        """
        return self.execute("select", sql, filter_values=filter_values)

    def insert(self, sql, values):
        """
        插入
        """
        return self.execute("insert", sql, values=values)

    def update(self, sql, values, filter_values):
        """
        更新
        """
        return self.execute(
            "update", sql, values=values, filter_values=filter_values)

    def delete(self, sql, filter_values):
        """
        删除
        """
        return self.execute("delete", sql, filter_values=filter_values)

    def close(self):
        """
        关闭连接
        """
        self.cursor.close()
        self.connection.close()


# 临时测试
if __name__ == "__main__":
    test_driver = Driver(
        type_="mysql",
        host="xxxxx",
        port=3306,
        username="root",
        password="xxxxx",
        database="xxxxx"
    )
    test_driver.connect()
    print(test_driver.test())
    test_driver.close()
