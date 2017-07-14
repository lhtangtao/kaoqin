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
from read_excel import duplicate_removal, overtime_money, get_init_date


def main(ID, start, end):
    # init_date = get_init_date() # 从excel中读取数据
    init_date = get_info_from_web(ID, start, end)  # 从浏览器中自动获取数据
    after = duplicate_removal(init_date)
    overtime_money(after)


if __name__ == '__main__':
    main(ID='000107063', start="2017/7/1", end="2017/7/13")
