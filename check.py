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
import types
import time
from datetime import datetime
import logs

# code here
__all__ = ["check_func"]


def cal_run_time(func):
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
        logs.log_info("Run %s<%s> costs time: %d ms" % (
        func.__name__, paras, (time4 - time3).seconds * 1000 + (time4 - time3).microseconds / 1000))
        return result

    return _cal


def check_func(file_name, class_name=None):
    """
        方法检查的装饰器
    """

    def _check(func):
        def __check(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                exc_type, exc_value, exc_tb = sys.exc_info()
                line_num = get_line_num(traceback.format_exc())
                line_str = ""
                if line_num > 0:
                    line_str = " line %d," % line_num
                if class_name:
                    error_msg = "BOOM!!! In File '%s',%s class[%s] - function<%s>" % (
                        str(file_name), line_str, str(class_name), func.__name__,)
                else:
                    error_msg = "BOOM!!! In File '%s',%s function <%s>" % (
                        str(file_name), line_str, func.__name__,)
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


def get_line_no(exc_tb):
    line_num = 0
    if exc_tb and isinstance(exc_tb, types.TracebackType):
        while exc_tb:
            if str(exc_tb.tb_frame.f_locals).find(".py") > -1:
                line_num = exc_tb.tb_lineno
            print(line_num, exc_tb.tb_frame.f_locals)
            exc_tb = exc_tb.tb_next
    return line_num


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

@cal_run_time
def run_1():
    for x in range(0,3):
        print(x)
        time.sleep(1)

@check_func(__file__)
def run_2():
    raise  Exception("my exception")

def main():
    run_1()

if __name__ == "__main__":
    main()
