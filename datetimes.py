# coding=utf-8
"""
datetime的帮助方法
"""
__author__ = 'kejun'
import datetime
import re
import time

from dateutil.parser import *

import check


@check.check_func(__file__)
def get_now(pattern=None):
    """
     get the current date time with predefine pattern
    :param pattern: datetime pattern,choices:'%Y-%m-%d %H:%M:%S','%m%d%y%H%M%S',...
    :return: current date time string, none if execute fail
    """
    if not pattern:
        pattern = '%Y-%m-%d %H:%M:%S'
    return time.strftime(pattern, time.localtime(time.time()))


@check.check_func(__file__)
def str2date(date_str):
    """
    transfer str to datetime
    :param date_str:date text
    :return:datetime object
    """
    return parse(date_str, default=datetime.datetime.now())


@check.check_func(__file__)
def time2str(time1, pattern):
    """
    transfer time to string
    :param time1:
    :param pattern:
    :return:
    """
    return time1.strftime(pattern, time1)


@check.check_func(__file__)
def get_date_pattern(date1):
    """
    try to get datetime pattern from input text
    :param date1:datetime text
    :return:datetime pattern
    """
    date1 = str(date1).strip()
    if re.match(r"\d\d\d\d-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}", date1):
        return "%Y-%m-%d %H:%M:%S"
    elif re.match(r"\d\d\d\d-\d{1,2}-\d{1,2}", date1):
        return "%Y-%m-%d"
    elif re.match(r"\d\d\d\d/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}", date1):
        return "%Y/%m/%d %H:%M:%S"
    elif re.match(r"\d\d\d\d/\d{1,2}/\d{1,2}", date1):
        return "%Y/%m/%d"
    elif re.match(r"\d\d/\d\d/\d\d \d{1,2}:\d{1,2}:\d{1,2}", date1):
        return "%m/%d/%y %H:%M:%S"
    elif re.match(r"\d\d/\d\d/\d\d", date1):
        return "%m/%d/%y"
    else:
        return None


@check.check_func(__file__)
def date2str(date1, pattern=None):
    """
    transfer from date to str
    :param date1: input datetime parameter
    :param pattern: input pattern string
    :return:string
    """

    if not pattern:
        pattern = "%Y-%m-%d %H:%M:%S"
    return date1.strftime(pattern)


@check.check_func(__file__)
def str2time(date1, pattern=None):
    """
    transfer from str to datetime
    :param date1:
    :param pattern:
    :return:
    """
    if not pattern:
        pattern = "%Y-%m-%d %H:%M:%S"
    return time.strptime(date1, pattern)


if __name__ == '__main__':
    print "datetime_io testing..."
    # print get_date_pattern("2015-12-10")
    dt = str2date("201517:07:00")
    # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print type(dt)
    # print dt
