# -*- coding: UTF-8 -*-
"""
File: email.py
邮件的接口
"""
from __future__ import division

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import configs
from check import check_func


# code here
class Email(object):
    @check_func(__file__, "Email")
    def __init__(self, file_name, section):
        self.para_dict = {}
        with configs.ConfigWrapper(file_name, "read") as config1:
            sections = config1.get_sections()
            if section not in sections:
                raise Exception("Section not found: %s" % section)
            self.para_dict = config1.get_option_dict(section)
        para_key = self.para_dict.keys()
        if not {"host", "user", "password"}.issubset(set(para_key)):
            raise Exception("Need [host, user, password, server], found: %s" % str(para_key))

    @check_func(__file__, "Email")
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
            msg = MIMEText(content, _subtype=type, _charset="utf8")
        else:
            msg = MIMEMultipart()
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        if not isinstance(subject, unicode):
            subject = unicode(subject)
        msg['Subject'] = subject
        msg['From'] = self.para_dict["user"] + "@" + self.para_dict["host"]
        msg['To'] = ";".join(to_list)
        if file_dict:
            body = MIMEText(content, _subtype=type, _charset="utf-8")
            msg.attach(body)
            coding = "gb2312"
            for (k, v) in file_dict.items():
                attach = MIMEText(open(v.decode("utf-8").encode("gb2312"), 'rb').read(), 'base64', coding)
                attach["Content-Type"] = 'application/octet-stream'
                attach["Content-Disposition"] = 'attachment; filename=' + k.decode("utf-8").encode(coding)
                msg.attach(attach)
        return self.send_action(to_list, msg)

    @check_func(__file__, "Email")
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
            server.connect(self.para_dict["server"])
            server.login(self.para_dict["user"], self.para_dict["password"])
            is_connect = True
            server.sendmail(self.para_dict["user"] + "@" + self.para_dict["host"], to_list, msg.as_string())
            return True
        except Exception as e:
            raise Exception("Send email action fail--" + str(e))
        finally:
            if server and is_connect:
                server.quit()
            del server


def main():
    EM = Email(file_name="../res/profiles/email.ini", section="UP-email")
    print EM.send_email(['hekejun@unionpay.com'], "测试邮箱设置", "这是测试邮件")
    # print EM.send_mail(['hekejun@unionpay.com'], "测试邮箱设置", "<a href='http://www.baidu.com'>百度</a>",isHtml=True)


if __name__ == "__main__":
    main()
