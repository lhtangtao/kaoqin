#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
import calendar
import argparse
import sys

from send_mail import send_email


def infos(ID, month, address):
    start = "2017/" + str(month) + "/1"
    end = "2017/" + str(month) + "/" + str(calendar.monthrange(2017, month)[1])
    init_date = get_info_from_web(ID, start, end)  # 从浏览器中自动获取数据
    after = duplicate_removal(init_date)
    info_to_send = overtime_money(after)
    print info_to_send
    # send_email(address, info_to_send)


if __name__ == '__main__':
    # name_list = ["0068491", "0072927", "0101835 ", "0109084 ", "0080154", "0107063","0091742"]
    # for i in range(0,len(name_list)):
    #     infos(ID=name_list[i], month=7)
    #     print "   "
    infos(ID=str(sys.argv[1]), month=int(sys.argv[2]), address=str(sys.argv[3]))
    # infos(0107063, 9, 'tt')
