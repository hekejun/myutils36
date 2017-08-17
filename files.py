# -*- coding: UTF-8 -*-
"""
File: files.py
文件操作的接口
"""
from __future__ import division

import os
import platform
import types

from check import check_func


@check_func(__file__)
def cmd_open(filename):
    """
    open the determined file through cmd command
    :param filename:
    :return:true if the command is successfully done; false if it failed.
    """
    if has_file(filename):
        command = "start " + filename
        os.system(command)
        return True
    else:
        return False


@check_func(__file__)
def has_file(filename):
    """
    check the file exisits
    :param filename: input filename, like 'D:/test.txt'
    :return:
    """
    return os.path.exists(filename)


@check_func(__file__)
def get_dir_files(path):
    """
    get the files in the dir path
    :param filename: input filename, like 'D:/'
    :return:
    """
    return os.listdir(path)


@check_func(__file__)
def get_curr_dir():
    """
    get the current dir of the working program
    :return:
    """
    return os.getcwd()


@check_func(__file__)
def get_curr_files(path=None):
    """
    get the given dir files, if parameter is none get the files in current working dir
    :return:
    """
    if not path:
        path = get_curr_dir()
    return os.listdir(path)


@check_func(__file__)
def get_file_size(filename):
    """
    get the size of the input file
    :param filename: string file dir +　filename
    :return: int value of the file size; -1 if the file not exist
    """
    return os.path.getsize(filename)


@check_func(__file__)
def delete_file(filename):
    """
    delete the input file
    :param filename:
    :return:
    """
    if has_file(filename):
        os.remove(filename)
        return True
    return False


@check_func(__file__)
def read_datalines(file_name, flag=None, delete_line_break=False):
    """
    read file into data lines
    :param file_name:
    :param flag:
    :return: data list[]
    """
    if not flag:
        flag = "r"
    with open(file_name, flag) as f:
        data = f.readlines()
        if delete_line_break:
            line_break = "\n" if platform.system().find("indows") > -1 else "\r\n"
            data = [line.strip(line_break) for line in data]
        return data


@check_func(__file__)
def write_datalists(file_name, data, flag=None, use_line_break=False):
    """
    write file with data lists. use line break depends on the system platform
    :param file_name:
    :param data:
    :param flag:
    :param use_line_break:
    :return:
    """
    if not isinstance(data, types.ListType):
        raise Exception("Input data is not ListType: %s" % str(data))
    if not flag:
        flag = "w+"
    if use_line_break:
        line_break = "\n" if platform.system().find("indows") > -1 else "\r\n"
        data = ["".join([line, line_break]) for line in data]
    with open(file_name, flag) as f:
        f.writelines(data)
        return True


def main():
    print("hello,world")
    # cmd_open("d:/py2.txt")
    # print get_curr_dir()
    # print get_curr_files()
    # data_list = ["1", "2"]
    # print write_datalists("d:/test.txt", data_list, use_line_break=True)
    # print read_datalines("d:/test.txt", delete_line_break=True)
    print(delete_file("d:/test.txt"))


if __name__ == "__main__":
    main()