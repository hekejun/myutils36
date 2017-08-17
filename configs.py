# -*- coding: UTF-8 -*-
"""
File: configs.py
读取配置文件的接口
"""
from __future__ import division

import configparser

import files
from check import check_func

__all__ = ["ConfigWrapper"]


class ConfigWrapper(object):
    def __init__(self, file_name, mode):
        self.config = Config(file_name, mode)

    def __enter__(self):
        return self.config

    def __exit__(self, type, value, traceback):
        self.config.save()
        del self.config


class Config(object):
    @check_func(__file__, "Config")
    def __init__(self, file_name, mode):
        self.cf = configparser.ConfigParser()
        self.file_name = file_name
        self.mode = mode
        if mode == "read":
            if not files.has_file(file_name):
                raise Exception("File not exisits: %s" % file_name)
            self.cf.read(file_name)

    @check_func(__file__, "Config")
    def save(self):
        """
        保存
        :return:
        """
        if self.mode == "write":
            self.cf.write(open(self.file_name, "w"))

    @check_func(__file__, "Config")
    def get_sections(self):
        """
        获得所有section的名称
        :return:
        """
        return self.cf.sections()

    @check_func(__file__, "Config")
    def get_options(self, section):
        """
        获得section的所有item的key
        :param section:
        :return:
        """
        return self.cf.options(section)

    @check_func(__file__, "Config")
    def get_option_items(self, section):
        """
        获得section的list对象
        :param section:
        :return:
        """
        return self.cf.items(section)

    @check_func(__file__, "Config")
    def get_option_dict(self, section):
        """
        获得section的dict对象
        :param section:
        :return:
        """
        return dict(self.get_option_items(section))

    @check_func(__file__, "Config")
    def write(self, section, paras):
        """
        把dict对象以section的名字写入配置文件，覆盖写入
        :param section:
        :param paras:
        :return:
        """
        self.cf.add_section(section)
        for k, v in paras.items():
            self.cf.set(section, str(k), str(v))
        return True


def main():
    print('hello,world')
    with ConfigWrapper("email.ini", "write") as config:
        config.write("s1", {"a": 1, "b": 2})
        config.write("s2", {"c": 1, "d": 2})

    with ConfigWrapper("email.ini", "read") as config:
        print(config.get_sections())
        print(config.get_options("s1"))
        print(config.get_option_items("s1"))
        print(config.get_option_dict("s1"))

if __name__ == "__main__":
    main()
