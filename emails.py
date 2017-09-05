# -*- coding: UTF-8 -*-
"""
File: emails.py
邮件的接口
"""
from __future__ import division

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import configs


# code here
class Email(object):
    def __init__(self, **kwargs):
        self.paras = {}
        if "filename" in kwargs:
            with configs.ConfigWrapper(kwargs.get("filename"), "read") as config:
                sections = config.get_sections()
                if kwargs.get("section") not in sections:
                    raise Exception("Section not found: %s" % kwargs.get("section"))
            self.paras = config.get_option_dict(kwargs.get("section"))
        else:
            self.paras = kwargs
        para_key = self.paras.keys()
        if not {"host", "user", "password"}.issubset(set(para_key)):
            raise Exception("Need [host, user, password, server], found: %s" % str(para_key))

    def send_email(self, to_list, subject, content, file_dict=None, isHtml=False):
        """
        将输入的信息进行构建，转化为email的messgae
        :param to_list: 接受地址
        :param subject: 邮件主题
        :param content: 邮件内容
        :param file_dict:附件列表
        :param isHtml:是否转成html格式文本
        :return:
        """
        type = 'plain'
        if isHtml:
            type = "html"
        if not file_dict:
            msg = MIMEText(content, _subtype=type, _charset="utf-8")
        else:
            msg = MIMEMultipart()
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        subject=subject.decode("utf-8")
        msg['Subject'] = subject
        msg['From'] = self.paras["user"] + "@" + self.paras["host"]
        msg['To'] = ";".join(to_list)
        if file_dict:
            body = MIMEText(content, _subtype=type, _charset="utf-8")
            msg.attach(body)
            coding = "gb2312"
            for (k, v) in file_dict.items():
                attach = MIMEText(open(v.decode("utf-8").encode(coding), 'rb').read(), 'base64', coding)
                attach["Content-Type"] = 'application/octet-stream'
                attach["Content-Disposition"] = 'attachment; filename=' + k.decode("utf-8").encode(coding)
                msg.attach(attach)
        return self.send_action(to_list, msg)

    def send_action(self, to_list, msg):
        """
        发送邮件操作
        :param to_list:
        :param msg:
        :return:
        """
        server, is_connect = "", False
        try:
            server = smtplib.SMTP()
            server.connect(self.paras["server"])
            server.login(self.paras["user"], self.paras["password"])
            is_connect = True
            server.sendmail(self.paras["user"] + "@" + self.paras["host"], to_list, msg.as_string())
            return True
        except Exception as e:
            raise Exception("Send email action fail--" + str(e))
        finally:
            if server and is_connect:
                server.quit()
            del server
