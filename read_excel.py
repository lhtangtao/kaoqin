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
        py_date = datetime.datetime(year, month, day, hour, minute)
        time_list.append(py_date)
    return sorted(time_list)  # 返回根据时间排序的列表


def duplicate_removal(date):
    """
    输入一个list，去除里面重复的时间段。
    :param date:
    :return:
    """
    date_len = len(date)  # 数组的长度
    number_to_del = []
    for i in range(date_len - 1):
        closing_time = date[i + 1]
        office_time = date[i]
        time_delay = (closing_time - office_time).seconds / 7200  # 时间差 以小时为单位
        if time_delay < 2:  # 时间差在一小时以内的，计算最新时间。 遇到重复时间，下班则取较晚的时间 上班则取较早的时间
            if office_time.hour < 13:
                number_to_del.append(i + 1)
            if closing_time.hour > 12:
                number_to_del.append(i)
    for i in range(len(number_to_del)):
        del date[number_to_del[i] - i]
    return date  # 返回去重后的数组


def overtime(after_duplicate_removal):
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
    for i in range(0, len(weekday_date), 2):
        if weekday_date[i + 1] - weekday_date[i] >= datetime.timedelta(hours=12):  # 加班超过三小时才算加班
            time_delay = weekday_date[i + 1] - weekday_date[i]
            overtime_day = time_delay - datetime.timedelta(hours=9)  # 当日加班时间
            overtime_day = str(overtime_day)
            if int(overtime_day.split(':')[1]) >= 30:  # 如果加班时间有半小时多出
                overtime_day_verbose = float(overtime_day.split(":")[0]) + 0.5
                weekday_overtime.append(overtime_day_verbose)
            else:
                overtime_day_verbose = float(overtime_day.split(":")[0])
                weekend_overtime.append(overtime_day_verbose)
    weekday_total = 0.0
    for i in range(len(weekday_overtime)):
        weekday_total = weekday_overtime[i] + weekday_total

    print u'工作日加班时长为：'+str(weekday_total)

    weekend_total = 0.0
    for i in range(len(weekend_overtime)):
        weekend_total = weekend_overtime[i] + weekend_total
    print u'周末加班时长为：' + str(weekend_total)

if __name__ == '__main__':
    init_date = get_init_date()
    after = duplicate_removal(init_date)
    overtime(after)
