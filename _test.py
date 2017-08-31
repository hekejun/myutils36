# -*- coding: UTF-8 -*-
"""
File: _test.py
测试utils包各功能函数的健壮性
"""
import sys
import platform
import time

import const
from check import check_func, cal_run_time
from configs import ConfigWrapper
from datetimes import *
from dbc import SqlWrapper
from logs import *
from emails import Email
from mongo import MongoWrapper
from pyredis import RedisHelper


def wrapper(func):
    def _wrapper(*args, **kwargs):
        print("Testing function {}...".format(func.__name__))
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print("Boom! {}".format(str(e)))
        print("Finish testing function {}".format(func.__name__))
        return result

    return _wrapper


@wrapper
def test_check():
    run_1()
    run_2()


@cal_run_time
def run_1():
    for x in range(0, 3):
        time.sleep(1)


@check_func(__file__)
def run_2():
    raise Exception("my exception")


@wrapper
def test_config():
    with ConfigWrapper("email1.ini", "write") as config:
        config.write("s1", {"a": 1, "b": 2})
        config.write("s2", {"c": 1, "d": 2})
    with ConfigWrapper("email1.ini", "read") as config:
        print(config.get_sections())
        print(config.get_options("s1"))
        print(config.get_option_items("s1"))
        print(config.get_option_dict("s1"))


@wrapper
def test_datetimes():
    print(get_date_pattern("2015-12-10"))
    now = get_now()
    print(now)
    print(type(str2date(now)))
    print(type(str2time(now)))
    dt_str = "2017-08-30 10:34:56"
    print(date2str(str2date(dt_str)))

@wrapper
def test_dbc():
    # with SqlWrapper(filename="mysql.ini", section="database_mysql") as sql_helper: #另外一种导入方式
    with SqlWrapper(host="127.0.0.1",server="test",user="test",password="test") as sql_helper:
        sql_helper.insert(table="role", col_list=["role_name", "role_desc"],
                          data_list=[[u"我们", u"不知道"], [u"我们w2", u"不知道q"]])
        print(sql_helper.select_one(table="role", col="id", where="id>5", order_by="id desc"))
        print(sql_helper.select_many(table="role", where="id>5", order_by="id desc"))
        print(sql_helper.update_many(table="role", col_list=["role_name", "role_desc"], data_list=["1", "2"],
                                          where="id>8"))
        print(sql_helper.update_one(table="role", col="role_name", value="33", where="id>10"))
        print(sql_helper.delete(table="role",where="id>=7"))

@wrapper
def test_logs():
    log_debug("debug")
    log_info("info")
    log_warnning("warnning")
    log_error("error")
    log_critical("critical")


@wrapper
def test_emails():
    EM = Email(filename="email.ini", section="UP-email")
    # print(EM.send_email(['hekejun@unionpay.com'], "测试邮箱设置", "这是测试邮件"))
    EM.send_email(['hekejun@unionpay.com'], "测试邮箱设置", "<a href='http://www.baidu.com'>百度</a>",isHtml=True)

@wrapper
def test_mongo():
    with MongoWrapper(host="127.0.0.1", database="temp") as mongo_helper:
        print(mongo_helper.get_collection_names())
        print(mongo_helper.update_value("temp", value={"cnt": 1}, where={"key": "d"}, increment=True))
        print(mongo_helper.update_value("temp",value={"count":1},where={"name":"a"},increment=True,only_one=True))
        print(mongo_helper.insert("abc", {"a": 112, "b": "blabla"}))
        print(mongo_helper.insert_many("abc",[{"a":113,"b":"haha"},{"a":119,"b":"huojing"}]))
        print(mongo_helper.insert("abc",{"a":111,"b":"bla"}))
        print(mongo_helper.remove("abcd",clear_all=True))
        print(mongo_helper.remove_collection("abcd"))
        print(mongo_helper.find("abc"))
        print(mongo_helper.select("abc",{"a":111},cols=["a"]))
        print(mongo_helper.count("abc"))
        print(mongo_helper.update("abc",value={"b":"new_word"},where={"a":112}))
        print(mongo_helper.update("abc",value={"b":1},where={"a":3},increment=True))
        print(mongo_helper.update("abc",value={"b":"new_word222"},where={"a":111}))
        print(mongo_helper.update("abc",value={"b":"new_word333"},where={"a":111},only_one=True))
        print(mongo_helper.replace("abc",where={"a":119},document={"e":22,"f":220}))
        print(mongo_helper.select("abc"))
        print(mongo_helper.remove("abc",where={"e":22}))
        print(mongo_helper.create_index("abc","a",name="index1"))


@wrapper
def test_redis():
    cache = RedisHelper()
    for i in range(10):
        cache.redis().mset({
            'blog:post:%s:title' % i: u'文章%s标题' % i,
            'blog:post:%s:content' % i: u'文章%s的正文' % i
        })
    post_list = []
    for i in range(10):
        post = cache.redis().mget('blog:post:%s:title' % i, 'blog:post:%s:content' % i)
        if post:
            post_list.append(post)
    for title, content in post_list:
        print(title, content)
    cache.redis().hset('blog:info', 'title', u'the5fire的技术博客')
    cache.redis().hset('blog:info', 'url', u'http://www.the5fire.com')
    blog_info_title = cache.redis().hget('blog:info', 'title')
    print(blog_info_title)
    blog_info = cache.redis().hgetall('blog:info')
    print(blog_info)
    cache.redis().hmset('blog:info', {
        'title': 'the5fire blog',
        'url': 'http://www.the5fire.com',
    })
    blog_info1 = cache.redis().hmget('blog:info', 'title', 'url')
    print(blog_info1)

if __name__ == '__main__':
    print("=======================")
    print("Python version:{0}.{1}.{2}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    print("System info:{0}, {1}".format(platform.system(), platform.architecture()[0]))
    # test_check()
    # test_config()
    # test_datetimes()
    # test_dbc()
    # test_logs()
    # test_emails()
    # test_mongo()
    test_redis()