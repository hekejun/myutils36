# -*- coding: UTF-8 -*-
"""
File: configs.py
读写配置文件的接口
"""
import configparser
import files
import codecs

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
    def __init__(self, filename, mode):
        self.cf = configparser.ConfigParser()
        self.filename = filename
        self.mode = mode
        if mode == "read":
            if not files.has_file(filename):
                raise Exception("File not exisits: %s" % filename)
            self.cf.read_file(codecs.open(filename, "r", "utf-8-sig"))

    def save(self):
        """
        保存
        :return:
        """
        if self.mode == "write":
            self.cf.write(codecs.open(self.filename, "w", "utf-8"))

    def get_sections(self):
        """
        获得所有section的名称
        :return:
        """
        return self.cf.sections()

    def get_options(self, section):
        """
        获得section的所有item的key
        :param section:
        :return:
        """
        return self.cf.options(section)

    def get_option_items(self, section):
        """
        获得section的list对象
        :param section:
        :return:
        """
        return self.cf.items(section)

    def get_option_dict(self, section):
        """
        获得section的dict对象
        :param section:
        :return:
        """
        return dict(self.get_option_items(section))

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
