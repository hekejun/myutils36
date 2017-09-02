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
