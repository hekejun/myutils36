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

