# -*- coding: UTF-8 -*-
"""
File: strings.py
string的帮助函数
"""
from __future__ import division

import datetimes,re
from check import check_func


@check_func(__file__)
def clean_text(text):
    if text and isinstance(text, basestring):
        return text.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "").replace(u"　", "").replace(
            "...", "").replace(u"", "").replace(u"", "")
    else:
        return ""

def transform_input(*args):
    """
    将输入的参数按照一定格式组成一个string
    :return:
    """
    if args:
        return "$cHATbOT*".join([str(x) for x in args])
    else:
        return ""

def transform_output(str1):
    if not str1:
        return []
    elif str1.find("$cHATbOT*")==-1:
        return [str1]
    else:
        return str1.split("$cHATbOT*")



@check_func(__file__)
def transfer_sql_text(text):
    """
    将一个未知数据类型的对象转换成string类型的sql文本，i.e.: 1->string(1) "a"->'a'
    :param text:
    :return:
    """
    if (not isinstance(text, float) and not isinstance(text, int) and not text) or (
                isinstance(text, basestring) and text.upper() == 'NONE'):
        return "''"
    elif str(type(text)) == "<type 'datetime.datetime'>":
        return "'" + datetimes.date2str(text) + "'"
    elif isinstance(text, basestring):
        return "'" + text.replace("'", "") + "'"
    else:
        return str(text)


@check_func(__file__)
def transfer_sql_list(text_list):
    """
    将一组未知数据类型的对象转成成sql文本，以","分隔
    :param text_list:
    :return:
    """
    text_list = [transfer_sql_text(text) for text in text_list]
    return ",".join(text_list)

def unicode(str1):
    if isinstance(str1,str):
        return str1.decode("utf-8")
    return str1

def utf8(str1):
    if not isinstance(str1,str) and isinstance(str1,basestring):
        return str1.encode("utf-8")
    return str1

def main():
    str1 = u"一"
    # print str1.isupper()
    # print is_chinese(str1)
    # print cns2digs(str1)
    # print get_email_content(u"中文中文bbbb.aaa@163.com中文hekejun@unionpay.com")

if __name__ == "__main__":
    main()
