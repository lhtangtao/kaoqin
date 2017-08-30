#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7.13
@author: tangtao
@contact: tangtao@lhtangtao.com
@description: 此处添加描述
@site: http://www.lhtangtao.com
@software: PyCharm
@file:  kaoqin

"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(mail_address, infos):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "993790934@qq.com"  # 用户名
    mail_pass = "jzlxkbruomkjbfei"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

    sender = '993790934@qq.com'
    receivers = [mail_address, '670076298@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(infos, 'plain', 'utf-8')
    message['From'] = Header("tangtao", 'utf-8')
    message['To'] = Header("user", 'utf-8')

    subject = u'吉利考勤情况'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print "send success"
    except smtplib.SMTPException, e:
        print e
