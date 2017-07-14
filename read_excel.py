#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7.13
@author: tangtao
@contact: tangtao@lhtangtao.com
@description: 此处添加描述
@site: http://www.lhtangtao.com
@software: PyCharm
@file: read_excel.py
@time: 2017/7/13 10:47
"""
import xlrd
from xlrd import xldate_as_tuple
import datetime
import time

from open_url import get_info_from_web


def get_init_date(source_book='attendance.xlsx'):
    """
    输入excel表格的名字 随后把所有读到的日期返回到一个list中
    :param source_book:
    :return:
    """
    book = xlrd.open_workbook(source_book)
    sh = book.sheet_by_name(u"Sheet1")
    time_list = []  # 原始的时间数据信息存放在此
    for i in range(1, sh.nrows):
        info = sh.row(i)
        year, month, day, hour, minute, second = xldate_as_tuple(info[2].value, book.datemode)
        py_date = datetime.datetime(year, month, day, hour, minute) - datetime.timedelta(
            hours=7)  # 因为是以每天早上七点为临界点，因此要扣除7个小时
        time_list.append(py_date)
    return time_list  # 返回根据时间排序的列表


def duplicate_removal(date):
    """
    输入一个list，去除里面重复的时间段。
    :param date:
    :return:
    """
    date = sorted(date)
    date_len = len(date)  # 数组的长度
    number_to_del = []
    for i in range(1, date_len - 1):
        if date[i].day == date[i - 1].day & date[i].day == date[i + 1].day:
            number_to_del.append(i)
    for i in range(len(number_to_del)):
        del date[number_to_del[i] - i]  # 删除重复的考勤记录
    return date  # 返回去重后的数组


def overtime_money(after_duplicate_removal):
    """
    计算加班情况
    :param after_duplicate_removal:
    :return:
    """
    weekday_date = []
    weekend_date = []
    for i in range(len(after_duplicate_removal)):
        if after_duplicate_removal[i].weekday() < 5:
            weekday_date.append(after_duplicate_removal[i])
        else:
            weekend_date.append(after_duplicate_removal[i])
    weekday_overtime = []
    weekend_overtime = []
    subsidy = 0  # 餐补
    for i in range(0, len(weekday_date), 2):  # 计算工作日的加班和餐补
        if weekday_date[i + 1] - weekday_date[i] >= datetime.timedelta(hours=11):  # 加班超过三小时才能拿餐补
            subsidy = subsidy + 15
        if weekday_date[i + 1] - weekday_date[i] >= datetime.timedelta(hours=12):  # 加班超过三小时才算加班
            time_delay = weekday_date[i + 1] - weekday_date[i]
            overtime_day = time_delay - datetime.timedelta(hours=9)  # 当日加班时间
            overtime_day = str(overtime_day)
            if int(overtime_day.split(':')[1]) >= 30:  # 如果加班时间有半小时多出
                overtime_day_verbose = float(overtime_day.split(":")[0]) + 0.5
                weekday_overtime.append(overtime_day_verbose)
            else:
                overtime_day_verbose = float(overtime_day.split(":")[0])
                weekday_overtime.append(overtime_day_verbose)
    for i in range(0, len(weekend_date), 2):  # 计算周末的加班和餐补
        if weekend_date[i + 1] - weekend_date[i] >= datetime.timedelta(hours=4):  # 加班超过三小时才能拿餐补
            subsidy = subsidy + 15
        time_delay_weekend = weekend_date[i + 1] - weekend_date[i]
        overtime_day_weekend = str(time_delay_weekend)
        if int(overtime_day_weekend.split(':')[1]) >= 30:  # 如果加班时间有半小时多出
            overtime_day_verbose = float(overtime_day_weekend.split(":")[0]) + 0.5
            weekend_overtime.append(overtime_day_verbose)
        else:
            overtime_day_verbose = float(overtime_day_weekend.split(":")[0])
            weekend_overtime.append(overtime_day_verbose)

    weekday_total = 0.0
    for i in range(len(weekday_overtime)):
        weekday_total = weekday_overtime[i] + weekday_total
    print u'工作日加班时长为：' + str(weekday_total)
    print u'餐补为：' + str(subsidy)
    weekend_total = 0.0
    for i in range(len(weekend_overtime)):
        weekend_total = weekend_overtime[i] + weekend_total
    print u'周末加班时长为：' + str(weekend_total)
