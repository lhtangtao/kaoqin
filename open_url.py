#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7.13
@author: tangtao
@contact: tangtao@lhtangtao.com
@description: 此处添加描述
@site: http://www.lhtangtao.com
@software: PyCharm
@file: open_url.py
@time: 2017/7/14 13:57
"""
from selenium import webdriver
import time
import datetime


def get_info_from_web(ID="000107063", start="2017/06/01", end="2017/06/30"):
    driver = webdriver.Chrome()
    driver.get("http://kaoqin.geely.auto/")
    driver.maximize_window()
    driver.find_element_by_id("UserId").clear()
    driver.find_element_by_id("UserId").send_keys(ID)
    driver.find_element_by_id("StartDate").clear()
    driver.find_element_by_id("StartDate").send_keys(start)
    driver.find_element_by_id("EndDate").clear()
    driver.find_element_by_id("EndDate").send_keys(end)
    time.sleep(1)
    driver.find_element_by_name("ctl07").click()  # 点击搜索按钮
    time.sleep(1)
    date_info = []
    for x in range(2, 12):
        xpath = ".//*[@id='GridView1']/tbody/tr[" + str(x) + "]/td[3]"
        info = driver.find_element_by_xpath(xpath).text
        date_info.append(info)
    page_total = len(
        driver.find_element_by_xpath(".//*[@id='GridView1']/tbody/tr[12]/td/table/tbody").find_elements_by_tag_name(
            "td"))  # 查看一共有几页信息
    for i in range(2, page_total):
        driver.find_element_by_link_text(str(i)).click()
        for x in range(2, 12):
            xpath = ".//*[@id='GridView1']/tbody/tr[" + str(x) + "]/td[3]"
            info = driver.find_element_by_xpath(xpath).text
            date_info.append(info)
        time.sleep(1)
    driver.find_element_by_link_text(str(page_total)).click()
    message = len(driver.find_element_by_xpath(".//*[@id='GridView1']/tbody").find_elements_by_tag_name(
        "tr")) - 3  # 查看这页一共有几行信息 目前看来是减少3
    for x in range(2, 2 + message):
        xpath = ".//*[@id='GridView1']/tbody/tr[" + str(x) + "]/td[3]"
        info = driver.find_element_by_xpath(xpath).text
        date_info.append(info)
    driver.quit()
    date_info_datetime = []
    for i in range(0, len(date_info)):
        date_info_datetime.append(datetime.datetime.strptime(date_info[i], '%Y/%m/%d %H:%M:%S') - datetime.timedelta(
            hours=7))
    return date_info_datetime


if __name__ == '__main__':
    print get_info_from_web()
