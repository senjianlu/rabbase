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


# 检索 SQL
SELECT_SQL = """
SELECT
    {_column_names}
FROM
    {_table_name}
WHERE
    {filter}
"""

# 插入 SQL
INSERT_SQL = """
INSERT INTO
    {_table_name}({_column_names})
VALUES(
    {insert_values}
) ON CONFLICT DO NOTHING
"""

# 更新 SQL
UPDATE_SQL = """
UPDATE
    {_table_name}
SET
    {update_values}
WHERE
    {filter}
"""

# 插入冲突时更新 SQL
INSERT_ON_CONFLICT_DO_UPDATE = """
INSERT INTO
    {_table_name}({_column_names})
VALUES(
    {insert_values}
) ON CONFLICT(
    {_primary_keys}
) DO UPDATE SET {update_values}
"""

# 删除 SQL
DELETE_SQL = """
DELETE FROM
    {table_name}
WHERE
    {filter}
"""


class BaseClass():
    """
    基础类
    """

    def __init__(self):
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
        for key in temp_dict.keys():
            if (key.startswith("_")):
                temp_dict.pop(key)
        self.__dict__.update(temp_dict)

    def _to_dict(self):
        """
        类转字典
        """
        temp_dict = copy.deepcopy(self.__dict__)
        for key in temp_dict.keys():
            if (key.startswith("_")):
                temp_dict.pop(key)
        return temp_dict

    def select(self):
        """
        检索
        """
        pass

    def insert(self):
        """
        插入
        """
        pass

    def update(self):
        """
        更新
        """
        pass

    def insert_on_conflict_do_update(self):
        """
        插入冲突时更新
        """

    def delete(self):
        """
        删除
        """
        pass


if __name__ == "__main__":
    """
    测试
    """
    test_base_class = BaseClass()
    print(test_base_class._column_names)
