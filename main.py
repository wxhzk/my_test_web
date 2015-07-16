#!/usr/bin/env python
#-*- coding:utf-8 -*-


import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options

import settings

#define语句一定要在parse_command_line之前执行完
define("port", default=8000, help="run on the given port", type=int)

def echo(message):
    print message

def main():
    tornado.options.parse_command_line()
    try:
        app = tornado.web.Application(handlers=settings.handlers, **settings.settings)
        srv = tornado.httpserver.HTTPServer(app)
        srv.listen(options.port)
        echo("listen on the port:%s"%options.port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        settings.mysql.stop()
    except:
        tornado.ioloop.IOLoop.instance().stop()
        settings.mysql.stop()
        raise


if __name__=='__main__':
    main()




