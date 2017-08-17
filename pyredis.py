# -*- coding: UTF-8 -*-
"""
File: redis_py.py
Created since 2017/5/3 15:54.
Author: Kejun.He
"""
from __future__ import division, absolute_import

from myutils import configs, const, const_values
from myutils.check import check_func
import redis
import types


class RedisHelper(object):
    __classname = "RedisHelper"

    @check_func(__file__, __classname)
    def __init__(self, **kwargs):
        """
        这里做了一个外壳来包装redis，好处：
        1.提供多重配置参数的输入，包括配置文件config读取等
        2.方便Singleton的调用。这样速度可以保证内存永远有一个redis接口提供调用，更快。
        :param kwargs:
        """
        if "filename" in kwargs:
            with configs.ConfigWrapper(kwargs.get("filename"), "read") as config:
                sections = config.get_sections()
                if kwargs.get("section", "NOTHING FOUND") not in sections:
                    raise Exception("Section not found: %s" % kwargs.get("section"))
            para_dict = config.get_option_dict(kwargs.get("section"))
        else:
            para_dict = kwargs
        _host = "localhost" if "host" not in para_dict else para_dict.get("host")
        _port = 6379 if "port" not in para_dict else int(para_dict.get("port"))
        _db = 0 if "database" not in para_dict else int(para_dict.get("database"))
        _pw = None if "password" not in para_dict else para_dict.get("password")
        self.__cursor = redis.StrictRedis(host=_host, port=_port, db=_db, password=_pw)

    @check_func(__file__, __classname)
    def redis(self):
        """
        返回reids接口
        :return:
        """
        return self.__cursor

    @check_func(__file__, __classname)
    def close(self):
        """
        关闭，其实没有什么效果，redis本身支持线程池调度，连接的启动关闭有线程池管理，python接口无需关心。
        The connection_pool object has a disconnect method to force
        an immediate disconnect of all connections in the pool if necessary
        :return:
        """
        del self.__cursor  # 删除引用，等待垃圾回收


def main():
    # redis_helper = RedisHelper(filename=const.project_main_path+r"\res\profiles\redis.ini",section="test_redis")
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
        print title, content
    cache.redis().hset('blog:info', 'title', u'the5fire的技术博客')
    cache.redis().hset('blog:info', 'url', u'http://www.the5fire.com')
    blog_info_title = cache.redis().hget('blog:info', 'title')
    print blog_info_title
    blog_info = cache.redis().hgetall('blog:info')
    print blog_info
    cache.redis().hmset('blog:info', {
        'title': 'the5fire blog',
        'url': 'http://www.the5fire.com',
    })
    blog_info1 = cache.redis().hmget('blog:info', 'title', 'url')
    print blog_info1


if __name__ == "__main__":
    main()
