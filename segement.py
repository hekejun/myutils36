# -*- coding: UTF-8 -*-
"""
File: segement.py
Created since 2017/5/2 15:08.
Author: Kejun.He
"""
from __future__ import division, absolute_import
import jieba
import const
import jieba.posseg as pseg


def min_cut(str1, dict1=None):
    if dict1:
        jieba.load_userdict(dict1)
    seg_list = jieba.lcut_for_search(str1)
    _result = []
    index = 0
    while index < len(seg_list):
        if index > 0:
            if len(seg_list[index]) == 3:  # 如果该词是三词，且覆盖前面，选择三词
                flag = get_word_flag(seg_list[index])
                if seg_list[index].find(seg_list[index - 1]) > -1 and (flag[0] == 'n' or flag in ["eng", "m"]):
                    if index > 1 and seg_list[index].find(seg_list[index - 2]) > -1:
                        _result = _result[:len(_result) - 2]
                    else:
                        _result = _result[:len(_result) - 1]
                    _result.append(seg_list[index])
                elif seg_list[index].find(seg_list[index - 1]) > -1 or (
                        index > 1 and seg_list[index].find(seg_list[index - 2]) > -1):
                    pass
                else:
                    _result.append(seg_list[index])
            else:
                if seg_list[index].find(seg_list[index - 1]) == -1:
                    _result.append(seg_list[index])
        else:
            _result.append(seg_list[index])
        index += 1
    return _result


def min_cut_flag(str1, dict1=None):
    _result = []
    _temp = min_cut(str1, dict1=dict1)
    if _temp:
        for word in _temp:
            # print word
            word_flag = pseg.cut(word)
            for w, f in word_flag:
                _result.append((w, f))
    return _result


def max_cut(str1,dict1=None):
    if dict1:
        jieba.load_userdict(dict1)
    return jieba.lcut(str1)


def max_cut_flag(str1, dict1=None):
    if dict1:
        jieba.load_userdict(dict1)
    _result = []
    words = pseg.cut(str1)
    if words:
        for w, f in words:
            _result.append((w, f))
    return _result


def get_word_flag(str1, dict1=None):
    if dict1:
        jieba.load_userdict(dict1)
    word_flag = pseg.cut(str1)
    _result = []
    if not word_flag:
        return "00"
    for w, f in word_flag:
        _result.append((w, f))
    if len(_result) == 1:
        return list(_result[0])[1]
    else:
        return "00"






def test_full():
    for temp_str in str_list:
        # print temp_str
        # seg_list = min_cut(temp_str)
        # print("MIN Mode: " + "/ ".join(seg_list))
        # seg_list = jieba.lcut_for_search(temp_str)
        # print("Search Mode: " + "/ ".join(seg_list))
        # print "-"*30
        for (w, flag) in min_cut_flag(temp_str):
            print w, flag
    str4 = u"在本地使用 27017 启动你的mongod服务。打开命令提示符窗口，进入MongoDB安装目录的bin目录输入命令mongodump？"
    for (w, flag) in min_cut_flag(str4):
        print w, flag
        # print "-"*50
        # for (w,flag) in max_cut_flag(str1):
        #     print w,flag


def test_dict():
    # jieba.suggest_freq("没")
    str1 = "在发卡系统升级时出现这个问题"
    jieba.load_userdict(const.project_main_path + r"\res\datas\testdict.txt")
    print ",".join(min_cut(str1))
    # print get_word_flag(str1,const.project_main_path+r"\res\datas\smalldict.txt")


def main():
    # print get_word_flag(u"澳大利")
    # print ",".join(min_cut(u"总裁"))
    # print get_word_flag(u"就是")
    # for k,v in min_cut_flag(U"你不应当这样子"):
    #     print k,v
    import sys,os
    print ("\\".join(os.getcwd().split("\\")[:-1]))
if __name__ == "__main__":
    main()
