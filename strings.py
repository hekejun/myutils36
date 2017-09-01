# -*- coding: UTF-8 -*-
"""
File: strings.py
string的帮助函数
"""
from __future__ import division

import datetimes,re



def transfer_sql_text(text):
    """
    将一个未知数据类型的对象转换成string类型的sql文本，i.e.: 1->string(1) "a"->'a'
    :param text:
    :return:
    """
    if (not isinstance(text, float) and not isinstance(text, int) and not text) or (
                isinstance(text, str) and text.upper() == 'NONE'):
        return "''"
    elif str(type(text)) == "<type 'datetime.datetime'>":
        return "'" + datetimes.date2str(text) + "'"
    elif isinstance(text, str):
        return "'" + text.replace("'", "") + "'"
    else:
        return str(text)


def transfer_sql_list(text_list):
    """
    将一组未知数据类型的对象转成成sql文本，以","分隔
    :param text_list:
    :return:
    """
    text_list = [transfer_sql_text(text) for text in text_list]
    return ",".join(text_list)

