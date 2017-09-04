# -*- coding: UTF-8 -*-
"""
File: mongo.py
Created since 2017/4/25 16:29.
Author: Kejun.He
"""
from __future__ import division, absolute_import

import types

from pymongo import MongoClient, ASCENDING, DESCENDING

import configs, const, const_values


# code here

class MongoWrapper(object):
    """
    SQL查询的接口
    """
    __slots__ = ["mongo_helper"]

    def __init__(self, **kwargs):
        self.mongo_helper = MongoHelper(**kwargs)

    def __enter__(self):
        return self.mongo_helper

    def __exit__(self, type, value, traceback):
        self.mongo_helper.close()
        del self.mongo_helper


class MongoHelper(object):
    __classname = "MongoHelper"

    def __init__(self, **kwargs):
        """
        设置mongo的连接池
        :param kwargs:
        """
        if "filename" in kwargs:
            with configs.ConfigWrapper(kwargs.get("filename"), "read") as config:
                sections = config.get_sections()
                if kwargs.get("section") not in sections:
                    raise Exception("Section not found: %s" % kwargs.get("section"))
            para_dict = config.get_option_dict(kwargs.get("section"))
        else:
            para_dict = kwargs
        para_key=para_dict.keys()
        if "database" not in para_key:
            raise Exception("Need database, found: %s" % str(para_key))
        _host="localhost" if "host" not in para_key else para_dict.get("host")
        _port = 27017 if "port" not in para_key else int(para_dict.get("port"))
        _max_pool = 100 if "max_pool" not in para_key else int(para_dict.get("max_pool"))
        _min_pool = 0 if "min_pool" not in para_key else int(para_dict.get("min_pool"))
        _connect_time = 20000 if "connect_time" not in para_key else int(para_dict.get("connect_time"))

        self.__client = MongoClient(host=_host, port=_port, maxPoolSize=_max_pool,
                                    minPoolSize=_min_pool, connectTimeoutMS=_connect_time)
        self.__db = self.__client.get_database(para_dict.get("database"))
        if "password" in para_key:
            self.__db.authenticate(para_dict.get("user"), para_dict.get("password"))

    def mongo(self):
        """
        返回mongo连接的实例对象
        :return:
        """
        return self.__db

    def get_collection_names(self):
        """
        获得mongodb中存在的集合名称
        :return:
        """
        return self.__db.collection_names()

    def insert(self, collection_name, values):
        """
        把文档插入集合
        :param collection_name:
        :param values:
        :return:
        """
        if values and not isinstance(values, dict):
            raise Exception(
                "Input parameter values should be dict type, get %s <%s> " % (str(values), str(type(values))))
        return self.__db.get_collection(collection_name).insert(values,check_keys=False)

    def insert_one(self, collection_name, values):
        if values and not isinstance(values, dict):
            raise Exception(
                "Input parameter values should be dict type, get %s <%s> " % (str(values), str(type(values))))
        return self.__db.get_collection(collection_name).insert_one(values)

    def insert_many(self, collection_name, values):
        if values and (not isinstance(values, list) or not isinstance(values[0], dict)):
            raise Exception("Input parameter values should be a list (includes dict values), get %s <%s> " % (
                str(values), str(type(values))))
        return self.__db.get_collection(collection_name).insert_many(values)

    def remove(self, collection_name, where=None):
        """
        删除集合中文档，可以根据过滤器where
        :param collection_name:
        :param where:
        :return:
        """
        if not where:
            where = {}
        elif where and not isinstance(where, dict):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        else:
            pass
        return self.__db.get_collection(collection_name).remove(where)

    def delete_collection(self, collection_name):
        return self.__db.drop_collection(collection_name)

    def create_collection(self, collection_name):
        return self.__db.create_collection(collection_name)

    def find(self, collection_name, where=None, cols=None, abandom_id=True, limit=0, skip=0, sort=None):
        """
        try to find a document from the given collection
        :param collection_name:
        :param where:
        :param cols:
        :param abandom_id:
        :param limit:
        :param skip:
        :param sort:
        :return:
        """
        if where and not isinstance(where, dict):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if sort and not isinstance(sort, dict):
            raise Exception("Input parameter sort should be dict type, get %s <%s> " % (str(sort), str(type(sort))))
        if cols and not isinstance(cols, list):
            raise Exception("Input parameter cols should be list type, get %s <%s> " % (str(cols), str(type(cols))))
        columns = {}
        if cols:
            for x in cols:
                columns[x] = True
            if abandom_id:
                columns["_id"] = False
            else:
                columns["_id"] = True
        else:
            columns=None
        if sort:
            sort = self.change_dict_tupleList(sort)

        return self.__db.get_collection(collection_name).find(filter=where, projection=columns, limit=limit, skip=skip,
                                                              sort=sort)

    def change_dict_tupleList(self, dict):
        res_list = []
        for (k, v) in dict.items():
            if v not in [1, -1]:
                raise Exception(
                    "Input parameter sort value should be integer 1('ASC') OR -1('DESC'), GET %s" % (str(v)))
            new_value = ASCENDING if v == 1 else DESCENDING
            res_list.append(tuple([k, new_value]))
        return res_list

    def count(self, collection_name, where=None):
        return self.find(collection_name, where=where).count()

    def select(self, collection_name, where=None, cols=None, limit=0, skip=0, sort=None,abandom_id=False):
        temp = self.find(collection_name, where=where, cols=cols, limit=limit, skip=skip, sort=sort,abandom_id=abandom_id)
        result = []
        if temp:
            for data in temp:
                result.append(data)
        return result

    def update_value(self, collection_name, where, value, only_one=False, increment=False, upsert=True):
        if not isinstance(where, dict):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(value, dict):
            raise Exception("Input parameter value should be dict type, get %s <%s> " % (str(value), str(type(value))))
        if increment:
            operator = "$inc"
        else:
            operator = "$set"
        new_dict = {operator: value}
        if only_one:
            return self.__db.get_collection(collection_name).update(where, new_dict, upsert=upsert)
        else:
            return self.__db.get_collection(collection_name).update_many(where, new_dict, upsert=upsert)

    def push(self,collection_name,where,value,allow_repeat=True):
        """
        insert or update a array field in the document given
        :param collection_name:
        :param where:
        :param value:
        :param allow_repeat: True means allow repeat filed values
        :return:
        """
        if not isinstance(where, dict):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(value, dict):
            raise Exception("Input parameter value should be dict type, get %s <%s> " % (str(value), str(type(value))))
        if not allow_repeat:
            new_dict = {"$addToSet": value}
        else:
            new_dict = {"$push": value}
        self.__db.get_collection(collection_name).update(where, new_dict, upsert=True)

    def pull(self,collection_name,where,value):
        """
        insert or update a array field in the document given
        :param collection_name:
        :param where:
        :param value:
        :param allow_repeat: True means allow repeat filed values
        :return:
        """
        if not isinstance(where, dict):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(value, dict):
            raise Exception("Input parameter value should be dict type, get %s <%s> " % (str(value), str(type(value))))
        new_dict = {"$pop": value}
        self.__db.get_collection(collection_name).update(where, new_dict, upsert=True)

    def replace_document(self, collection_name, document, where, upsert=True):
        if not isinstance(where, dict):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(document, dict):
            raise Exception(
                "Input parameter document should be dict type, get %s <%s> " % (str(document), str(type(document))))
        return self.__db.get_collection(collection_name).replace_one(where, document, upsert=upsert)

    def create_index(self, collection_name, index, name=None, unique=False, background=False):
        if not isinstance(index, dict) and not isinstance(index, str):
            raise Exception("Input parameter index should be dict type or basestring, get %s <%s> " % (
                str(index), str(type(index))))
        if isinstance(index, dict):
            index = self.change_dict_tupleList(index)
        return self.__db.get_collection(collection_name).create_index(index, name=name, unique=unique,
                                                                      background=background)

    def drop_index(self, collection_name, index_or_name):
        return self.__db.get_collection(collection_name).drop_index(index_or_name)

    def close(self):
        if self.__client:
            del self.__client