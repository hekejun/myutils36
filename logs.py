# -*- coding: UTF-8 -*-
"""
File: logs.py
日志输出的接口
"""
from __future__ import division
import logging
import const,const_values

__all__ = ["log_debug", "log_info", "log_warnning", "log_error", "log_critical"]

# 基本配置
logging.basicConfig(level=const.log_file_level,
                    format='%(asctime)s %(filename)s-line:%(lineno)d [%(levelname)s] : %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S',
                    filename=const.log_file_name ,
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(const.log_console_level)
formatter = logging.Formatter('%(asctime)s %(filename)s-line:%(lineno)d [%(levelname)s] : %(message)s')
console.setFormatter(formatter)
my_logger = logging.getLogger('')
my_logger.addHandler(console)


# 对外使用的log接口
def log_debug(msg, *args, **kwargs):
    """
    输出bug信息
    :param msg:
    :param args:
    :param kwargs:
    :return:
    """
    my_logger.debug(msg, *args, **kwargs)


def log_info(msg, *args, **kwargs):
    """
    输出info信息
    :param msg:
    :param args:
    :param kwargs:
    :return:
    """
    my_logger.info(msg, *args, **kwargs)


def log_warnning(msg, *args, **kwargs):
    """
    输出warnning信息
    :param msg:
    :param args:
    :param kwargs:
    :return:
    """
    my_logger.warning(msg, *args, **kwargs)


def log_error(msg, *args, **kwargs):
    """
    输出error信息
    :param msg:
    :param args:
    :param kwargs:
    :return:
    """
    my_logger.error(msg, *args, **kwargs)


def log_critical(msg, *args, **kwargs):
    """
    输出critical信息
    :param msg:
    :param args:
    :param kwargs:
    :return:
    """
    my_logger.critical(msg, *args, **kwargs)


