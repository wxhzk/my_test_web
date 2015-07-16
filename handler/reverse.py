#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])






