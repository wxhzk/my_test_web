#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', "NNN")
        self.write("Hello,"+name)








