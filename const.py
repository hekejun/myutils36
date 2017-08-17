# -*- encoding:UTF-8 -*-
"""
常量的创建类
"""
__author__ = 'kejun'


# create Datetime: 15-11-22 下午5:01

class _const(object):
    """
    常量类，设置变量不可被修改
    """

    def __setattr__(self, k, v):
        if k in self.__dict__:
            raise Exception("Const value should not be change.")
        else:
            self.__dict__[k] = v


import sys

sys.modules[__name__] = _const()
