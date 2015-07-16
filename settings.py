#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

from handler import hello
from handler import reverse
from handler import login
from handler import register

from utils import async_mysql

db_config = {
    "host"   : '127.0.0.1',
    "user"   : 'root',
    "passwd" : 'mysql_pass',
    "db"     : 'mydb',
    "charset": 'utf8',
}

mysql = async_mysql.AsyncMySQL(db_config)

handlers = [
    (r'/hello', hello.HelloHandler),
    (r'/reverse/(?P<input>\w+)', reverse.ReverseHandler),
    (r'/login', login.LoginHandler, dict(mysql=mysql)),
    (r'/register', register.RegisterHandler, dict(mysql=mysql)),
]

settings = {
    "debug": True,
    "static_path": os.path.join(os.path.dirname(__file__), 'static'),
    "template_path": os.path.join(os.path.dirname(__file__), 'template'),
}







