#!/usr/bin/env python
#-*- coding:utf-8 -*-

import _mysql

class MySQL(object):
    def __init__(self, host, user, passwd, db, charset, **kwargs):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db
        self._charset = charset
        self._kwargs = kwargs
        self.connect()

    def connect(self):
        self._mysql = _mysql.connect(host=self._host, user=self._user, passwd=self._passwd, db=self._db)
        self.autocommit()
        self.set_charset()

    def close(self):
        self._mysql.close()

    def autocommit(self, option=True):
        self._mysql.autocommit(option)

    def set_charset(self, charset=None):
        charset = charset or self._charset
        self._mysql.set_character_set(charset)

    def ping(self):
        self._mysql.ping()

    def select_db(self, db):
        self._mysql.select_db(db)

    def use_result(self):
        return self._mysql.use_result()

    def store_result(self):
        return self._mysql.store_result()

    def insert_id(self):
        return self._mysql.insert_id()

    def affected_rows(self):
        return self._mysql.affected_rows()

    def execute(self, sql):
        try:
            self.ping()
        except _mysql.OperationalError:
            self.connect()
        res = None
        try:
            res = self._mysql.query(sql)
        except _mysql.OperationalError as e:
            args = [arg for arg in e.args]
            args.append(sql)
            raise _mysql.OperationalError(*args)
        return res

    def query(self, sql, how=1):
        res = []
        self.execute(sql)
        result = self.store_result()
        rows = result.fetch_row(maxrows=100, how=how)
        while len(rows)>0:
            res.extend(rows)
            rows = result.fetch_row(maxrows=100, how=how)
        return res

    def select(self, sql, how=1):
        self.execute(sql)
        result = self.store_result()
        rows = result.fetch_row(maxrows=100, how=how)
        while len(rows)>0:
            for row in rows:
                yield row
            rows = result.fetch_row(maxrows=100, how=how)

    def insert(self, sql):
        self.execute(sql)
        return self.insert_id()

    def update(self, sql):
        self.execute(sql)
        return self.affected_rows()

    def delete(self, sql):
        self.execute(sql)
        return self.affected_rows()

    def count(self, sql, field='NUM'):
        return self.query(sql)[0][field]

    @staticmethod
    def escape_string(s):
        if isinstance(s, (int, long, float)):
            return str(s)
        elif isinstance(s, unicode):
            return "'%s'"%_mysql.escape_string(s.encode("UTF-8"))
        elif isinstance(s, basestring):
            return "'%s'"%_mysql.escape_string(s)
        return ''

    @staticmethod
    def construct_where(where_dict={}):
        if not where_dict:
            return ' 1=1 '
        if not isinstance(where_dict, dict):
            raise ValueError("where_dict must be dict instance")
        return ' AND '.join(["`%s`=%s"%(k, MySQL.escape_string(where_dict[k])) for k in where_dict.keys()])

    @staticmethod
    def construct_insert(table, value_dict):
        if not (value_dict and isinstance(value_dict, dict)):
            raise ValueError("value_dict must be dic instance")
        sql = "INSERT INTO `{0}`({1}) VALUES ({2})"
        keys = value_dict.keys()
        fields = ','.join(["`%s`"%k for k in keys])
        values = ','.join(["%s"%MySQL.escape_string(value_dict[k]) for k in keys])
        return sql.format(table, fields, values)

    @staticmethod
    def construct_select(table, fields=['*'], where_dict={}):
        sql = "SELECT {0} from `{1}` WHERE {2}"
        fields = fields or ['*']
        if not isinstance(fields, (list, tuple)):
            fields = [fields]
        fields = ','.join(fields)
        where = MySQL.construct_where(where_dict)
        return sql.format(fields, table, where)

    @staticmethod
    def construct_update(table, update_dict, where_dict={}):
        sql = "UPDATE `{0}` SET {1} WHERE {2}"
        values = ','.join(["`%s`=%s"%(k, MySQL.escape_string(update_dict[k])) for k in update_dict.keys()])
        where = MySQL.construct_where(where_dict)
        return sql.format(table, values, where)

    @staticmethod
    def construct_delete(table, where_dict={}):
        sql = "DELETE FROM `{0}` WHERE {1}"
        where = MySQL.construct_where(where_dict)
        return sql.format(table, where)

    @staticmethod
    def construct_count(table, where_dict={}):
        sql = "SELECT COUNT(*) AS NUM FROM `{0}` WHERE {1}"
        where = MySQL.construct_where(where_dict)
        return sql.format(table, where)


