#!/usr/bin/env python
#-*- coding:utf-8 -*-
import tornado.web
from base import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        accid = self.get_cookie('accid')
        if accid:
            self.write("accid:%s"%(accid))
        else:
            self.render("login.html")

    @tornado.web.asynchronous
    def post(self):
        acc = self.get_argument("account", None)
        passwd = self.get_argument("password", None)
        success = False
        if (acc and passwd):
            success = True
            self.mysql.query('account', ['id',], {'account': acc, 'passwd': passwd}, callback=self.callback)
        if not success:
            self.write("账号或密码错误，请重新登陆")
            self.set_status(401)
            self.finish()

    def callback(self, result, err):
        print 'in login callback (%s, (%s))'%(result, err)
        if not err and result:
            self.write("登陆成功")
            self.set_cookie('accid', result[0]['id'])
            self.set_status(200)
            self.finish()
        else:
            self.write("登陆失败")
            self.set_status(401)
            self.finish()







