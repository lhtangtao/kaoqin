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
        if date[i].day == date[i - 1].day and date[i].day == date[i + 1].day:  # 删除重复的考勤记录
            number_to_del.append(i)
        if date[i].day != date[i - 1].day and date[i].day != date[i + 1].day:  # 删除只有一次打卡记录的数据，一天只打一次卡就当作为大卡处理
            number_to_del.append(i)
    for i in range(len(number_to_del)):
        del date[number_to_del[i] - i]  # 删除重复的考勤记录
    if date[0].day != date[1].day:  # 如果第一天只有一个考勤记录则删除
        del date[0]
    date_len = len(date)
    if date[date_len - 1].day != date[date_len - 2].day:  # 如果最后一天只有一天考勤记录则删除
        del date[date_len - 1]
    for z in range(len(date)):
        print date[z] + datetime.timedelta(
            hours=7)
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
            print u'work start：' + str(weekday_date[i] + datetime.timedelta(hours=7)) + u'work end：' + str(
                weekday_date[i + 1] + datetime.timedelta(hours=7)) + u'weekday overtime' + str(overtime_day)
            weekday_overtime.append(overtime_day)
            # if int(overtime_day.split(':')[1]) >= 30:  # 如果加班时间有半小时多出
            #     overtime_day_verbose = float(overtime_day.split(":")[0]) + 0.5
            #     weekday_overtime.append(overtime_day_verbose)
            # else:
            #     overtime_day_verbose = float(overtime_day.split(":")[0])
            #     weekday_overtime.append(overtime_day_verbose)
    for i in range(0, len(weekend_date), 2):  # 计算周末的加班和餐补
        if weekend_date[i + 1] - weekend_date[i] >= datetime.timedelta(hours=4):  # 周末加班超过4小时才能拿餐补
            subsidy = subsidy + 15
            if weekend_date[i + 1] - weekend_date[i] >= datetime.timedelta(hours=8):
                subsidy = subsidy + 15
        time_delay_weekend = weekend_date[i + 1] - weekend_date[i]
        overtime_day_weekend = time_delay_weekend
        print u'work start：' + str(weekend_date[i] + datetime.timedelta(hours=7)) + u'work end：' + str(
            weekend_date[i + 1] + datetime.timedelta(hours=7)) + u'weekend overtime：' + str(overtime_day_weekend)
        weekend_overtime.append(overtime_day_weekend)
        # if int(overtime_day_weekend.split(':')[1]) >= 30:  # 如果加班时间有半小时多出
        #     overtime_day_verbose = float(overtime_day_weekend.split(":")[0]) + 0.5
        #     weekend_overtime.append(overtime_day_verbose)
        # else:
        #     overtime_day_verbose = float(overtime_day_weekend.split(":")[0])
        #     weekend_overtime.append(overtime_day_verbose)
    weekday_total = weekday_overtime[0]
    for i in range(1, len(weekday_overtime)):
        weekday_total = weekday_overtime[i] + weekday_total
    print 'weekday initial data is :'+str(weekday_total)
    day_to_hour = int(weekday_total.days) * 24
    real_hour = float(weekday_total.seconds)/3600+float(day_to_hour)
    info1 = u'weekday add:   ' + str(real_hour)+'H'
    info2 = u'money to eat:   ' + str(subsidy)
    if len(weekend_overtime) != 0:
        weekend_total = weekend_overtime[0]
        for i in range(1, len(weekend_overtime)):
            weekend_total = weekend_overtime[i] + weekend_total
        print 'weekend initial data is :' + str(weekend_total)
        end_to_hour=int(weekend_total.days) * 24
        real_end_hour=float(weekend_total.seconds)/3600+float(end_to_hour)
        info3 = u'weekend add:   ' + str(real_end_hour)
        info = info1 + '\n' + info2 + '\n' + info3+'H'
    else:
        info = info1 + '\n' + info2
    return info
