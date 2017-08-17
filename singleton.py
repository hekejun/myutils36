# -*- coding: UTF-8 -*-
"""
File: singleton.py
Created since 2017/4/26 17:08.
Author: Kejun.He
"""
from __future__ import division

import threading

import const, const_values
from dbc import SqlHelper
from mongo import MongoHelper
from pyredis import RedisHelper


class Singleton(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = {}

    @classmethod
    def instance(cls, **kwargs):
        if "instance" not in kwargs:
            raise Exception("Singleton method<instance> need a parameter: 'instance'.")
        with cls.__singleton_lock:
            if not cls.__singleton_instance.has_key(kwargs["instance"]):
                if kwargs.get("instance") == "mysql":
                    cls.__singleton_instance["mysql"] = SqlHelper(**kwargs)
                elif kwargs.get("instance") == "mongo":
                    cls.__singleton_instance["mongo"] = MongoHelper(**kwargs)
                elif kwargs.get("instance") == "redis":
                    cls.__singleton_instance["redis"] = RedisHelper(**kwargs)
                else:
                    return None
        return cls.__singleton_instance[kwargs.get("instance")]


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
def main():
    # c = Singleton().instance(instance="mysql",filename= "../res/profiles/mysql.ini", section="mysql_server")
    # d = Singleton().instance(instance="mysql",filename= "../res/profiles/mysql.ini", section="mysql_server")
    # j = Singleton().instance(instance="mysql",filename= "../res/profiles/mysql.ini", section="mysql_server")
    # args_dict={"instance":"mysql","filename":"../res/profiles/mysql.ini","section":"mysql_server"}
    # h=Singleton().instance(**args_dict)
    # m=Singleton.instance(**const.test_mongo_paras)
    # assert c is d
    # assert j is c
    # assert h is d
    # assert m is c
    # print c.select_one(table="role",col="count(*)")
    # print m.select_one(table="role",col="id")
    # print d.select_one(table="book",col="count(*)",where="get!=1")
    # print j.select_one(table="book",col="count(*)",where="get=1")
    # c.close()
    # d.close()

    e = Singleton().instance(instance="mongo", filename=const.project_main_path + "/res/profiles/mongo.ini",
                             section="test_mongo")
    f = Singleton().instance(instance="mongo", filename=const.project_main_path + "/res/profiles/mongo.ini",
                             section="test_mongo")
    g = Singleton().instance(instance="mongo", filename=const.project_main_path + "/res/profiles/mongo.ini",
                             section="test_mongo")
    h = Singleton().instance(instance="mongo", filename=const.project_main_path + "/res/profiles/mongo.ini",
                             section="test_mongo")
    print (e is f)
    print (e is g)
    print (e is h)
    print e.get_collection_names()
    print f.get_collection_names()
    print g.get_collection_names()
    print h.get_collection_names()
    e.close()
    f.close()


if __name__ == "__main__":
    main()
