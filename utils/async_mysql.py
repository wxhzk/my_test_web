#!/usr/bin/env python
#-*- coding:utf-8 -*-

from utils.mysql import MySQL
from utils.async_mixin import TaskThread, AsyncMixin, async_class

class MySQLTask(TaskThread):
    def __init__(self, *args, **kwargs):
        self._mysql = MySQL(**kwargs["db_config"])
        super(MySQLTask,self).__init__(*args, **kwargs)
        self.daemon = True

    def get_handler(self):
        return self._mysql

    def close(self):
        self._mysql.close()

@async_class
class AsyncMySQL(AsyncMixin):
    __async_methods__ = ['query', 'select', 'insert', 'update', 'delete', 'count']

    def __init__(self, db_config, **kwargs):
        kwargs['taskargs'] = {"db_config": db_config} 
        kwargs['taskclass'] = MySQLTask
        super(AsyncMySQL, self).__init__(**kwargs)

    def query(self, table, fields=['*'], where_dict={}, callback=None):
        sql = MySQL.construct_select(table, fields, where_dict)
        return (sql,)

    def select(self, table, fields=['*'], where_dict={}, callback=None):
        sql = MySQL.construct_select(table, fields, where_dict)
        return (sql,)

    def insert(self, table, value_dict, callback=None):
        sql = MySQL.construct_insert(table, value_dict)
        return (sql,)

    def update(self, table, update_dict, where_dict={}, callback=None):
        sql = MySQL.construct_update(table, update_dict, where_dict)
        return (sql, )

    def delete(self, table, where_dict={}, callback=None):
        sql = MySQL.construct_delete(table, where_dict)
        return (sql,)

    def count(self, table, where_dict={}, callback=None):
        sql = MySQL.construct_count(table, where_dict)
        return (sql,)

    def close(self):
        self.stop()









