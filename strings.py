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

def unicode(str1):
    if isinstance(str1,str):
        return str1.decode("utf-8")
    return str1

def utf8(str1):
    if not isinstance(str1,str) and isinstance(str1,str):
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
