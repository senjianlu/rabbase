#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: ~/GitHub/rabbase/orm.py
# @DATE: 2022/08/14 周日
# @TIME: 13:45:56
#
# @DESCRIPTION: ORM 模块


import copy

import rab_database


# 检索 SQL
SELECT_SQL = """
SELECT
    {_column_names}
FROM
    {_table_name}
WHERE
    {filters_placeholder}
"""

# 插入 SQL
INSERT_SQL = """
INSERT INTO
    {_table_name}({_column_names})
VALUES(
    {insert_values_placeholder}
) ON CONFLICT DO NOTHING
"""

# 更新 SQL
UPDATE_SQL = """
UPDATE
    {_table_name}
SET
    {update_values_placeholder}
WHERE
    {filters_placeholder}
"""

# 插入冲突时更新 SQL
INSERT_ON_CONFLICT_DO_UPDATE = """
INSERT INTO
    {_table_name}({_column_names})
VALUES(
    {insert_values_placeholder}
) ON CONFLICT(
    {_primary_keys}
) DO UPDATE SET {update_values_placeholder}
"""

# 删除 SQL
DELETE_SQL = """
DELETE FROM
    {_table_name}
WHERE
    {filters_placeholder}
"""


class BaseClass():
    """
    基础类
    """

    def __init__(self, _table_name, _primary_keys):
        """
        初始化
        """
        # 主键 ID
        self.id = None
        self.create_user = None
        self.create_time = None
        self.update_user = None
        self.update_time = None
        # 表相关
        self._table_name = None
        self._primary_keys = ["id"]
        self._column_names = self._get_column_names()

    def _get_column_names(self) -> list:
        """
        获取类的所有字段
        """
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    def _to_class(self, dict_):
        """
        字典转类
        """
        temp_dict = copy.deepcopy(dict_)
        for key in dict_.keys():
            if (key.startswith("_")):
                temp_dict.pop(key)
        self.__dict__.update(temp_dict)

    def _to_dict(self):
        """
        类转字典
        """
        temp_dict = copy.deepcopy(self.__dict__)
        for key in self.__dict__.keys():
            if (key.startswith("_")):
                temp_dict.pop(key)
        return temp_dict

    def select(self, database_driver: rab_database.Driver):
        """
        检索

        默认根据本对象的主键进行搜索，某主键为空的时候会跳过该主键。
        """
        # 筛选用的参数 ["1 = 1", "column_01 = %s"]
        filters = ["1 = 1"]
        # 筛选实际用的值
        filter_values = []
        _dict = self._to_dict()
        for key in _dict.keys():
            if (key in self._primary_keys):
                value = _dict[key]
                # 主键有值才作为筛选条件
                if (value is not None):
                    filters.append(f"{key} = %s")
                    filter_values.append(value)
                else:
                    pass
            else:
                pass
        # 拼接检索 SQL
        select_sql = SELECT_SQL.format(
            _column_names=", ".join(self._column_names),
            _table_name=self._table_name,
            filters_placeholder="\nAND ".join(filters))
        # print(select_sql, "\n", filter_values)
        return database_driver.select(select_sql, filter_values)

    def insert(self, database_driver: rab_database.Driver):
        """
        插入

        返回成功插入的条数。
        """
        # 插入用的值
        _dict = self._to_dict()
        insert_values = [_dict[key] for key in self._column_names]
        # 拼接插入 SQL
        insert_sql = INSERT_SQL.format(
            _table_name=self._table_name,
            _column_names=", ".join(self._column_names),
            insert_values_placeholder=", ".join(
                ["%s"]*len(self._column_names)))
        # print(insert_sql, "\n", insert_values)
        return database_driver.insert(insert_sql, insert_values)

    def update(self, database_driver: rab_database.Driver):
        """
        更新

        返回成功更新的条数；只保留主键更新整条数据。
        """
        # 筛选用的参数
        filters = ["1 = 1"]
        # 筛选实际用的值
        filter_values = []
        _dict = self._to_dict()
        for key in _dict.keys():
            if (key in self._primary_keys):
                value = _dict[key]
                # 主键有值才作为筛选条件
                if (value is not None):
                    filters.append(f"{key} = %s")
                    filter_values.append(value)
                else:
                    pass
            else:
                pass
        # 更新用的值
        update_values = []
        update_values_placeholder_elements = []
        _dict = self._to_dict()
        for key in self._column_names:
            if (key not in self._primary_keys):
                update_values.append(_dict[key])
                update_values_placeholder_elements.append(f"{key} = %s")
        # 拼接更新 SQL
        update_sql = UPDATE_SQL.format(
            _table_name=self._table_name,
            update_values_placeholder=", ".join(
                update_values_placeholder_elements),
            filters_placeholder="\nAND ".join(filters))
        # print(update_sql, "\n", update_values, "\n", filter_values)
        return database_driver.update(update_sql, update_values, filter_values)

    def insert_on_conflict_do_update(self,
                                     database_driver: rab_database.Driver):
        """
        插入冲突时更新

        返回成功插入或更新的条数。
        """
        update_values_placeholder_elements = []
        _dict = self._to_dict()
        for key in self._column_names:
            if (key not in self._primary_keys):
                update_values_placeholder_elements.append(
                    f"{key} = excluded.{key}")
        insert_values = [_dict[key] for key in self._column_names]
        insert_on_conflict_do_update_sql = INSERT_ON_CONFLICT_DO_UPDATE.format(
            _table_name=self._table_name,
            _column_names=", ".join(self._column_names),
            insert_values_placeholder=", ".join(
                ["%s"]*len(self._column_names)),
            _primary_keys=", ".join(self._primary_keys),
            update_values_placeholder=", ".join(
                update_values_placeholder_elements))
        # print(insert_on_conflict_do_update_sql, "\n", insert_values)
        return database_driver.execute(
            "insert_on_conflict_do_update",
            insert_on_conflict_do_update_sql,
            insert_values)

    def delete(self, database_driver: rab_database.Driver):
        """
        删除

        返回删除的条数。
        """
        # 筛选用的参数
        filters = ["1 = 1"]
        # 筛选实际用的值
        filter_values = []
        _dict = self._to_dict()
        for key in _dict.keys():
            if (key in self._primary_keys):
                value = _dict[key]
                # 主键有值才作为筛选条件
                if (value is not None):
                    filters.append(f"{key} = %s")
                    filter_values.append(value)
                else:
                    pass
            else:
                pass
        # 拼接删除用 SQL
        delete_sql = DELETE_SQL.format(
            _table_name=self._table_name,
            filters_placeholder="\nAND ".join(filters))
        # print(delete_sql, "\n", filter_values)
        return database_driver.delete(delete_sql, filter_values)


# 临时测试
if __name__ == "__main__":
    import uuid
    import datetime
    # 建立数据库连接
    test_database_driver = rab_database.Driver(
        type_="postgresql",
        host="xxxxx",
        port=5432,
        username="postgres",
        password="xxxxx",
        database="xxxxx"
    )
    test_database_driver.connect()
    # 测试对象
    test_base_class = BaseClass("test", ["id"])
    # 测试检索
    # print(test_base_class.select(test_database_driver))
    # 测试插入
    # test_base_class.id = uuid.uuid1().hex
    # test_base_class.create_user = "test_user"
    # test_base_class.create_time = datetime.datetime.now(
    #     datetime.timezone.utc)
    # print(test_base_class.insert(test_database_driver))
    # 测试更新
    # count, select_result = test_base_class.select(test_database_driver)
    # test_base_class._to_class(select_result[0])
    # test_base_class.update_user = "test_user"
    # test_base_class.update_time = datetime.datetime.now(
    #     datetime.timezone.utc)
    # print(test_base_class.update(test_database_driver))
    # 测试删除
    # count, select_result = test_base_class.select(test_database_driver)
    # test_base_class._to_class(select_result[0])
    # print(test_base_class.delete(test_database_driver))
    # 测试冲突时更新
    test_base_class.id = uuid.uuid1().hex
    test_base_class.create_user = "test_user"
    test_base_class.create_time = datetime.datetime.now(
        datetime.timezone.utc)
    print(test_base_class.insert_on_conflict_do_update(test_database_driver))
    count, select_result = test_base_class.select(test_database_driver)
    test_base_class._to_class(select_result[0])
    test_base_class.create_user = "changed_test_user"
    print(test_base_class.insert_on_conflict_do_update(test_database_driver))
    # 关闭数据库连接
    test_database_driver.close()
