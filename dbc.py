# -*- coding: UTF-8 -*-
"""
mysql的读取接口，注意使用SQLWrapper来操作。
包括了SQL注入的防御措施。
"""
from __future__ import division

import MySQLdb as mysql
import configs
from logs import log_info

__all__ = ["SqlWrapper"]


# code here
class SqlWrapper(object):
    """
    SQL查询的接口
    """
    __slots__ = ["sql_helper"]

    def __init__(self, **kwargs):
        self.sql_helper = SqlHelper(**kwargs)

    def __enter__(self):
        return self.sql_helper

    def __exit__(self, type, value, traceback):
        self.sql_helper.close()
        del self.sql_helper


class Sql(object):
    __slots__ = ['__is_login', '__filepath', '__filename', '__database', "__is_normal"]
    _connect0 = ""

    def __init__(self, **kwargs):
        """
        从配置文件中读取参数，要求必须要有host, user, password, server配置，读取配置后连接数据库
        :param file_name:配置文件名
        :param section:配置参数的指定位置
        """
        if "filename" in kwargs:
            with configs.ConfigWrapper(kwargs.get("filename"), "read") as config:
                sections = config.get_sections()
                if kwargs.get("section") not in sections:
                    raise Exception("Section not found: %s" % kwargs.get("section"))
            para_dict = config.get_option_dict(kwargs.get("section"))
        else:
            para_dict = kwargs

        para_key = list(para_dict.keys())
        if not {"host", "user", "password", "server"}.issubset(set(para_key)):
            raise Exception("Need [host, user, password, server], found: %s" % str(para_key))

        self._connect0 = mysql.connect(host=para_dict.get("host"), user=para_dict.get("user"),
                                       passwd=para_dict.get("password"), db=para_dict.get("server"), charset='utf8')
        __cursor0 = self._connect0.cursor()
        __cursor0.run("SET NAMES utf8")
        self._connect0.commit()

    def close(self):
        """
        close mysql connect
        :return:
        """
        if self._connect0:
            self._connect0.close()

    def run(self, sql, data):
        """
        execute mysql statement with not result return
        :param sql:
        :param data:
        :return:
        """
        cur = self._connect0.cursor()
        if cur:
            cur.executemany(sql, data)
            self._connect0.commit()
            return True
        return False

    def fetch(self, sql, data, mode=None, size=-1):
        """
        execute sql statement and fetch some results back
        :param sql:
        :param mode:
        :param size:
        :return:
        """
        cur = self._connect0.cursor()
        if cur:
            cur.run(sql, data)
            if mode == "_MANY" and len > 0:
                data_list = cur.fetchmany(size=size)
            elif mode == "_ONE" and len == -1:
                data_list = cur.fetchone()
            else:
                data_list = cur.fetchall()
            return data_list
        return None


class SqlHelper(Sql):
    def __init__(self, **kwargs):
        super(SqlHelper, self).__init__(**kwargs)

    def insert(self, table, col_list, data_list):
        """
        insert data_list into data table
        :param table: data table
        :param col_list: parameters list
        :param format_list: the format list of each parameter
        :param data_list: the data list for each parameter
        :return: True if the sql execute successfully or False
        """
        if data_list and len(col_list) != len(data_list[0]):
            raise Exception(u"Size not match:col_list {0} ,data_list {1}".format(len(col_list), len(data_list[0])))
        data_list = [tuple(data) for data in data_list]
        sql = "insert into " + table + "(" + ",".join(col_list) + ") values(" + ",".join(["%s"] * len(col_list)) + ")"
        log_info("Sql: {0}, input: {1}".format(sql, data_list))
        return super(SqlHelper, self).run(sql, data_list)

    def delete(self, table, where=None, data=()):
        """
        execute the delete sql on the data table
        :param table: the target data table
        :param where: the condition sql part if needed
        :param data: the input data for filter sql
        :return: True if the sql execute successfully or False
        """
        sql = "delete from " + table
        if where:
            if not data or not isinstance(data, tuple):
                raise Exception("Need data with tuple format for delete sql execute.")
            sql += " where " + where
        log_info("Sql: {0}, input: {1}".format(sql, data))
        return super(SqlHelper, self).run(sql, data)

    def update(self, table, col, value, where=None):
        """
        update the data table with given value on a col
        :param table: the data table
        :param col: column will be changed
        :param value: value will be changed
        :param where: the condition sql part
        :return:True if the sql execute successfully or False
        """
        sql = "update " + table + " set " + col + " = %s"
        data = tuple(value)
        if where:
            sql += " where " + where
        log_info("Sql: {0}, input: {1}".format(sql, data))
        return super(SqlHelper, self).run(sql, data)

    def update_many(self, table, col_list, data_list, where=None):
        """
        update data on many columns
        :param table: the data table
        :param col_list: columns names
        :param data_list: new values for the columns
        :param where: the condition part of sql
        :return:True if the sql execute successfully or False
        """
        sql = "update " + table + " set "
        if len(col_list) != len(data_list):
            raise Exception(u"Size not match: col_list size--%d ,data_list size--%d" % len(col_list), len(data_list))
        new_datas = tuple(data_list)
        pairs = []
        for col in col_list:
            pairs.append("{0} = %s".format(col))
        sql += " , ".join(pairs)
        if where:
            sql += " where " + where
        log_info("Sql: {0}, input: {1}".format(sql, new_datas))
        return super(SqlHelper, self).run(sql, new_datas)

    def select_many(self, table, col=None, where=None, data=(), order_by=None, group_by=None):
        """
        select some values from table
        :param table: data table
        :param col: columns in data table, if not col, use * instead
        :param where:
        :param data:
        :param order_by:
        :param group_by:
        :return:
        """
        if col:
            sql = "select " + col + " from " + table
        else:
            sql = "select * from " + table
        if where:
            if not data or not isinstance(data, tuple):
                raise Exception("Need data with tuple format for select sql execute.")
            sql += " where " + where
        if group_by:
            sql += " group by " + group_by
        if order_by:
            sql += " order by " + order_by
        log_info("Sql: {0}, input: {1}".format(sql, data))
        result = super(SqlHelper, self).fetch(sql, data)
        return [list(x) for x in result]

    def filter(self, table, col=None, where=None, order_by=None, group_by=None):
        if not col or (col.upper().find("CONCAT") == -1 and col.find(",") > -1):
            raise Exception("Input Column name INVALID: %s!" % col)
        temp = self.select_many(table=table, col=col, where=where, order_by=order_by, group_by=group_by)
        result = [x[0] for x in temp]
        return result
