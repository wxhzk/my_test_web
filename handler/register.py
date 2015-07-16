#!/usr/bin/env python
#-*- coding:utf-8 -*-
import tornado.web
from base import BaseHandler

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    @tornado.web.asynchronous
    def post(self):
        account = self.get_argument("account")
        pass1 = self.get_argument("pass1")
        pass2 = self.get_argument("pass2")
        success = False
        if account and pass1==pass2 and len(pass1)>=6:
            success = True
            self.mysql.insert("account", {"account":account,"passwd":pass1},callback=self.callback)
        if not success:
            self.write("账号已存在或密码错误")
            self.set_status(401)
            self.finish()

    def callback(self, result, err):
        if not err:
            self.set_cookie('accid', str(result))
            self.write("注册成功")
            self.set_status(200)
            self.finish()
        else:
            self.write("注册失败")
            self.set_status(401)
            self.finish()










