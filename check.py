# -*- coding: UTF-8 -*-
"""
File: check.py
创建方法的检查使用的装饰器
"""
from __future__ import division

import platform
import re
import sys
import traceback
from datetime import datetime
import logs
from functools import wraps

# code here
__all__ = ["check_func", "cal_run_time"]


def cal_run_time(func):
    """
    计算函数的运行时间
    :param func:装饰函数名
    :return:返回函数运行结果
    """
    @wraps(func)
    def _cal(*args, **kwargs):
        time3 = datetime.utcnow()
        result = func(*args, **kwargs)
        time4 = datetime.utcnow()
        paras = ""
        if args:
            paras += ", ".join([str(x) for x in args])
        if kwargs:
            if paras:
                paras += "--"
            paras += ", ".join([str(x) for x in kwargs.values()])
        logs.log_info("Function <%s> costs time: %d ms" % (
            func.__name__, (time4 - time3).seconds * 1000 + (time4 - time3).microseconds / 1000))
        return result
    return _cal


def check_func(file_name=None):
    """
        方法检查的装饰器
        获得
    """
    def _check(func):
        @wraps(func)
        def __check(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                if file_name:
                    line_num = get_line_num(traceback.format_exc())
                    line_str = ""
                    if line_num > 0:
                        line_str = " line %d," % line_num
                    error_msg = "BOOM!!! In File '%s' %s - function<%s>" % (
                        str(file_name), line_str, func.__name__,)
                else:
                    error_msg = "BOOM!!! In function <%s>" % (func.__name__,)
                logs.log_error(error_msg)
                # 输出错误详情
                logs.log_error("Error details-- %s, %s" % (exc_type.__name__, exc_value))
                # 输出输入参数
                if args:
                    logs.log_error("Input Parameters-- %s" % str(args))
                if kwargs:
                    logs.log_error("Input K-V Parameters-- %s" % str(kwargs))
                # 输出详情信息
                logs.log_debug("%s" % traceback.format_exc())
                # 设置空行，方便浏览
                line_break = "\n" if platform.system().find("indows") > -1 else "\r\n"
                logs.log_error(line_break)
                return None

        return __check

    return _check


def get_line_num(exc_msg):
    """
    从报错信息中提取错误行号
    :param exc_msg: 报错信息
    :return: 错误行号
    """
    line_num = 0
    groups = re.findall(r'line \d+', exc_msg)
    # print groups
    if groups:
        if len(groups) >= 2:
            if groups[1].find(" ") > -1:
                line_num = int(groups[1].split(" ")[1])
        else:
            if groups[0].find(" ") > -1:
                line_num = int(groups[0].split(" ")[1])
    return line_num
