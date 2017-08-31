# -*- coding: UTF-8 -*-
"""
mysql的读取接口，注意使用SQLWrapper来操作
"""
from __future__ import division

import MySQLdb as mysql
import configs
import strings
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
    __slots__ = [ '__is_login', '__filepath', '__filename', '__database', "__is_normal"]
    __connect0 = ""

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

        self.__connect0 = mysql.connect(host=para_dict.get("host"), user=para_dict.get("user"),
                                        passwd=para_dict.get("password"), db=para_dict.get("server"), charset='utf8')
        __cursor0 = self.__connect0.cursor()
        __cursor0.execute("SET NAMES utf8")
        self.__connect0.commit()

    def close(self):
        """
        close mysql connect
        :return:
        """
        if self.__connect0:
            self.__connect0.close()

    def execute_sql(self, sql, data=None):
        """
        execute mysql statement with not result return
        :param sql:
        :param data:
        :return:
        """
        cur = self.__connect0.cursor()
        if cur:
            if not data:
                cur.execute(sql)
            else:
                cur.executemany(sql, data)
            self.__connect0.commit()
            return True
        return False

    def fetch_sql(self, sql, mode=None, size=-1):
        """
        execute sql statement and fetch some results back
        :param sql:
        :param mode:
        :param size:
        :return:
        """
        cur = self.__connect0.cursor()
        if cur:
            cur.execute(sql)
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
        log_info("SqlHelper run insert statement: {0},{1}".format(sql, ",".join(data_list[0])))
        return super(SqlHelper, self).execute_sql(sql, data_list)

    def delete(self, table, where=None):
        """
        execute the delete sql on the data table
        :param table: the target data table
        :param where: the condition sql part if needed
        :return: True if the sql execute successfully or False
        """
        sql = "delete from " + table
        if where:
            sql += " where " + where
        log_info("SqlHelper run delete statement: {}".format(sql))
        return super(SqlHelper, self).execute_sql(sql)

    def update_one(self, table, col, value, where=None):
        """
        update the data table with given value on a col
        :param table: the data table
        :param col: column will be changed
        :param value: value will be changed
        :param where: the condition sql part
        :return:True if the sql execute successfully or False
        """
        my_value = strings.transfer_sql_text(value)
        sql = "update " + table + " set " + col + " = " + my_value + ""
        if where:
            sql += " where " + where
        log_info("SqlHelper run update statement: {}".format(sql))
        return super(SqlHelper, self).execute_sql(sql)

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
            raise Exception(u"Size not match: col_list size--%d ,data_list size--%d" %len(col_list), len(data_list))
        pairs = []
        for i in range(0, len(col_list)):
            pairs.append(col_list[i] + " = " + strings.transfer_sql_text(data_list[i]))
        sql += " , ".join(pairs)
        if where:
            sql += " where " + where
        log_info("SqlHelper run update_many statement: {}".format(sql))
        return super(SqlHelper, self).execute_sql(sql)

    def select_many(self, table, col=None, where=None, order_by=None, group_by=None):
        """
        select some values from table
        :param table: data table
        :param col: columns in data table, if not col, use * instead
        :param where:
        :param order_by:
        :param group_by:
        :return:
        """
        if col:
            sql = "select " + col + " from " + table
        else:
            sql = "select * from " + table
        if where:
            sql += " where " + where
        if group_by:
            sql += " group by " + group_by
        if order_by:
            sql += " order by " + order_by
        log_info("SqlHelper run select statement:{}".format(sql))
        result = super(SqlHelper, self).fetch_sql(sql)
        return [list(x) for x in result]

    def select_one(self, table, col=None, where=None, order_by=None, group_by=None):
        if not col or (col.upper().find("CONCAT") == -1 and col.find(",") > -1):
            raise Exception("Input Column name INVALID: %s!" % col)
        temp = self.select_many(table=table, col=col, where=where, order_by=order_by, group_by=group_by)
        result = [x[0] for x in temp]
        return result
