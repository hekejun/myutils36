# -*- coding: UTF-8 -*-
"""
File: mongo.py
Created since 2017/4/25 16:29.
Author: Kejun.He
"""
from __future__ import division, absolute_import

import types

from pymongo import MongoClient, ASCENDING, DESCENDING

from myutils import configs, const, const_values
from myutils.check import check_func


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

    @check_func(__file__, __classname)
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

    @check_func(__file__, __classname)
    def mongo(self):
        """
        返回mongo连接的实例对象
        :return:
        """
        return self.__db

    @check_func(__file__, __classname)
    def get_collection_names(self):
        """
        获得mongodb中存在的集合名称
        :return:
        """
        return self.__db.collection_names()

    @check_func(__file__, __classname)
    def insert(self, collection_name, values):
        """
        把文档插入集合
        :param collection_name:
        :param values:
        :return:
        """
        if values and not isinstance(values, types.DictionaryType):
            raise Exception(
                "Input parameter values should be dict type, get %s <%s> " % (str(values), str(type(values))))
        return self.__db.get_collection(collection_name).insert(values,check_keys=False)

    @check_func(__file__, __classname)
    def insert_one(self, collection_name, values):
        if values and not isinstance(values, types.DictionaryType):
            raise Exception(
                "Input parameter values should be dict type, get %s <%s> " % (str(values), str(type(values))))
        return self.__db.get_collection(collection_name).insert_one(values)

    @check_func(__file__, __classname)
    def insert_many(self, collection_name, values):
        if values and (not isinstance(values, types.ListType) or not isinstance(values[0], types.DictionaryType)):
            raise Exception("Input parameter values should be a list (includes dict values), get %s <%s> " % (
                str(values), str(type(values))))
        return self.__db.get_collection(collection_name).insert_many(values)

    @check_func(__file__, __classname)
    def remove(self, collection_name, where=None):
        """
        删除集合中文档，可以根据过滤器where
        :param collection_name:
        :param where:
        :return:
        """
        if not where:
            where = {}
        elif where and not isinstance(where, types.DictionaryType):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        else:
            pass
        return self.__db.get_collection(collection_name).remove(where)

    @check_func(__file__, __classname)
    def delete_collection(self, collection_name):
        return self.__db.drop_collection(collection_name)

    @check_func(__file__, __classname)
    def create_collection(self, collection_name):
        return self.__db.create_collection(collection_name)

    # @check_func(__file__, __classname)
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
        if where and not isinstance(where, types.DictionaryType):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if sort and not isinstance(sort, types.DictionaryType):
            raise Exception("Input parameter sort should be dict type, get %s <%s> " % (str(sort), str(type(sort))))
        if cols and not isinstance(cols, types.ListType):
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

    @check_func(__file__, __classname)
    def count(self, collection_name, where=None):
        return self.find(collection_name, where=where).count()



    # @check_func(__file__, __classname)
    def select(self, collection_name, where=None, cols=None, limit=0, skip=0, sort=None,abandom_id=False):
        temp = self.find(collection_name, where=where, cols=cols, limit=limit, skip=skip, sort=sort,abandom_id=abandom_id)
        result = []
        if temp:
            for data in temp:
                result.append(data)
        return result

    # @check_func(__file__, __classname)
    def update_value(self, collection_name, where, value, only_one=False, increment=False, upsert=True):
        if not isinstance(where, types.DictionaryType):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(value, types.DictionaryType):
            raise Exception("Input parameter value should be dict type, get %s <%s> " % (str(value), str(type(value))))
        if increment:
            operator = "$inc"
        else:
            operator = "$set"
        new_dict = {operator: value}
        if only_one:
            return self.__db.get_collection(collection_name).update_one(where, new_dict, upsert=upsert)
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
        if not isinstance(where, types.DictionaryType):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(value, types.DictionaryType):
            raise Exception("Input parameter value should be dict type, get %s <%s> " % (str(value), str(type(value))))
        if not allow_repeat:
            new_dict = {"$addToSet": value}
        else:
            new_dict = {"$push": value}
        self.__db.get_collection(collection_name).update_one(where,new_dict,upsert=True)

    def pull(self,collection_name,where,value):
        """
        insert or update a array field in the document given
        :param collection_name:
        :param where:
        :param value:
        :param allow_repeat: True means allow repeat filed values
        :return:
        """
        if not isinstance(where, types.DictionaryType):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(value, types.DictionaryType):
            raise Exception("Input parameter value should be dict type, get %s <%s> " % (str(value), str(type(value))))
        new_dict = {"$pop": value}
        self.__db.get_collection(collection_name).update_one(where,new_dict,upsert=True)

    @check_func(__file__, __classname)
    def replace_document(self, collection_name, document, where, upsert=True):
        if not isinstance(where, types.DictionaryType):
            raise Exception("Input parameter where should be dict type, get %s <%s> " % (str(where), str(type(where))))
        if not isinstance(document, types.DictionaryType):
            raise Exception(
                "Input parameter document should be dict type, get %s <%s> " % (str(document), str(type(document))))
        return self.__db.get_collection(collection_name).replace_one(where, document, upsert=upsert)

    @check_func(__file__, __classname)
    def create_index(self, collection_name, index, name=None, unique=False, background=False):
        if not isinstance(index, types.DictionaryType) and not isinstance(index, types.StringType):
            raise Exception("Input parameter index should be dict type or basestring, get %s <%s> " % (
                str(index), str(type(index))))
        if isinstance(index, types.DictionaryType):
            index = self.change_dict_tupleList(index)
        return self.__db.get_collection(collection_name).create_index(index, name=name, unique=unique,
                                                                      background=background)

    @check_func(__file__, __classname)
    def drop_index(self, collection_name, index_or_name):
        return self.__db.get_collection(collection_name).drop_index(index_or_name)

    @check_func(__file__, __classname)
    def close(self):
        if self.__client:
            del self.__client
            # self.__client.close()


# noinspection PyUnresolvedReferences
def main():

    with MongoWrapper(host="127.0.0.1", database="person") as mongo_helper:
        print "start"
        # print mongo_helper.get_collection_names()
        # mongo_helper.update_value("temp", where={"previous": "a", "next": "b"}, value={"value": 1}, increment=True,
        #                           only_one=True)
        # mongo_helper.update_value("temp", where={"previous": "a", "next": "b"}, value={"value": 1}, increment=True,
        #                           only_one=True)
        # mongo_helper.update_value("temp", where={"previous": "a", "next": "b"}, value={"value": 1}, increment=True,
        #                           only_one=True)
        # mongo_helper.update_value("temp", where={"previous": "a", "next": "b"}, value={"value": 1}, increment=True,
        #                           only_one=True)
        # mongo_helper.update_value("temp", where={"previous": "c", "next": "b"}, value={"value": 1}, increment=True,
        #                           only_one=True)
        # data=mongo_helper.select("temp",cols=["previous","next"],abandom_id=True)
        # print str(data[0]["_id"])
        # from bson.objectid import ObjectId
        # data=mongo_helper.select("kbs",where={"_id":ObjectId("59227da39f058d1a4cbc92f6")},cols=["title"])
        # print data[0]["title"]
        temp=mongo_helper.select("portrait",cols=["mail"],abandom_id=True)
        print temp
        # with MongoWrapper(filename=const.project_main_path + "/res/profiles/mongo.ini",
        #                   section="test_mongo") as mongo_helper:
        #     print "start"
        #     print mongo_helper.get_collection_names()
        # print mongo_helper.update_or_insert("temp", value={"cnt": 1}, where={"key": "d"}, increment=True)
        # print mongo_helper.update_value("temp",value={"count":1},where={"name":"a"},increment=True,only_one=True)
        # print mongo_helper.insert("abc", {"a": 112, "b": "blabla"})
        # print mongo_helper.create_collection("up-faq")
        # print mongo_helper.create_collection("up-pages")
        # print mongo_helper.insert_many("abc",[{"a":113,"b":"haha"},{"a":119,"b":"huojing"}])
        # print mongo_helper.insert("abc",{"a":111,"b":"bla"})
        # print mongo_helper.remove("abcd",clear_all=True)
        # print mongo_helper.remove_collection("abcd")
        # print mongo_helper.find("abc")
        # print mongo_helper.select("abc",{"a":111},cols=["a"])
        # print mongo_helper.select("abc",cols=["a","b"],where={"a":{"$gte":4}})
        # print mongo_helper.select("abc",limit=2,skip=1,sort=[("b",DESCENDING)])
        # print mongo_helper.select("abc",sort={"a":-1,"b":-1})
        # print mongo_helper.select("abc",sort={"a":-1,"b":1})
        # print mongo_helper.select("abc", sort={"a": -1, "b": 0})
        # print mongo_helper.count("abc")
        # print mongo_helper.update("abc",value={"b":"new_word"},where={"a":112})
        # print mongo_helper.update("abc",value={"b":1},where={"a":3},increment=True)
        # print mongo_helper.update("abc",value={"b":"new_word222"},where={"a":111})
        # print mongo_helper.update("abc",value={"b":"new_word333"},where={"a":111},only_one=True)
        # print mongo_helper.replace("abc",where={"a":119},document={"e":22,"f":220})
        # print mongo_helper.select("abc")
        # print mongo_helper.remove("abc",where={"e":22})
        # print mongo_helper.create_index("abc","a",name="index1")


if __name__ == "__main__":
    main()
