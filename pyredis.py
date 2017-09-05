# -*- coding: UTF-8 -*-
"""
File: redis_py.py
Created since 2017/5/3 15:54.
Author: Kejun.He
"""
from __future__ import division, absolute_import

import configs
import redis


class RedisHelper(object):
    __classname = "RedisHelper"

    def __init__(self, **kwargs):
        """
        这里做了一个外壳来包装redis，好处：
        1.提供多重配置参数的输入，包括配置文件config读取等
        2.方便Singleton的调用。这样速度可以保证内存永远有一个redis接口提供调用，更快。
        :param kwargs:
        """
        if "filename" in kwargs:
            with configs.ConfigWrapper(kwargs.get("filename"), "read") as config:
                sections = config.get_sections()
                if kwargs.get("section", "NOTHING FOUND") not in sections:
                    raise Exception("Section not found: %s" % kwargs.get("section"))
            para_dict = config.get_option_dict(kwargs.get("section"))
        else:
            para_dict = kwargs
        _host = "localhost" if "host" not in para_dict else para_dict.get("host")
        _port = 6379 if "port" not in para_dict else int(para_dict.get("port"))
        _db = 0 if "database" not in para_dict else int(para_dict.get("database"))
        _pw = None if "password" not in para_dict else para_dict.get("password")
        self.__cursor = redis.StrictRedis(host=_host, port=_port, db=_db, password=_pw)

    def redis(self):
        """
        返回reids接口
        :return:
        """
        return self.__cursor

    def close(self):
        """
        关闭，除了清除对象内存外没有什么效果，redis本身支持线程池调度，连接的启动关闭有线程池管理，python接口无需关心。
        The connection_pool object has a disconnect method to force
        an immediate disconnect of all connections in the pool if necessary
        :return:
        """
        del self.__cursor  # 删除引用，等待垃圾回收

    def set(self,*args):
        return self.__cursor.set(*args)

    def get(self,*args):
        return self.__cursor.get(*args)

    def lpush(self,*args):
        return self.__cursor.lpush(*args)

