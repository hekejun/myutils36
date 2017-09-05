# -*- coding: UTF-8 -*-
"""
项目使用的常量定义表
"""

import const
import logging
import sys

# ===========enviroment values start=============#
# 定义console的logging的报错级别
const.log_console_level = logging.INFO
const.log_file_level = logging.DEBUG
const.log_file_name = "run.log"

# 判断当前运行的python版本
const.env_py3 = True if sys.version_info.major == 3 else False

# ===========enviroment values end=============#