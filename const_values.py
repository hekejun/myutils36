# -*- coding: UTF-8 -*-
"""
项目使用的常量定义表
"""
import logging
import os

import const

"""
定义所需要的全部常量配置
"""
const.test_value=1

# 定义console的logging的报错级别
const.log_level_console = logging.INFO
const.log_level_file = logging.INFO
const.log_file_name="run.log"


def main():
    print(const.test_value)


if __name__ == "__main__":
    main()

