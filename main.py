#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7.13
@author: tangtao
@contact: tangtao@lhtangtao.com
@description: 此处添加描述
@site: http://www.lhtangtao.com
@software: PyCharm
@file: main.py
@time: 2017/7/14 15:14
"""
from open_url import get_info_from_web
from read_excel import duplicate_removal, overtime_money

if __name__ == '__main__':
    # init_date = get_init_date()
    init_date = get_info_from_web(start="2017/7/1", end="2017/7/13")
    after = duplicate_removal(init_date)
    overtime_money(after)
