# coding:utf8

import sys
import traceback
from threading import local
import _mysql


class MysqlConnManager(local):
    """
    This manager keeps that per thread resuses a private mysql connection,
    the connection is checked before executed and never shared with other
    threads or processes.
    """

    def __init__(self, host, port, db, usr, pwd):
        self._host = host
        self._port = port
        self._db = db
        self._usr = usr
        self._pwd = pwd
        self._conn = None

    def get_connection(self):
        if not self._is_conn_vaild():
            self._create_conn()
            if not self._is_conn_vaild():
                raise "Create MYSQL Connection Failed"
        return self._conn

    # def __del__(self):
        # if self._is_conn_vaild():
        # self._conn.close()

    def _create_conn(self):
        if self._is_conn_vaild():
            return
        self._conn = _mysql.connect(host=self._host,
                                    port=self._port,
                                    db=self._db,
                                    user=self._usr,
                                    passwd=self._pwd)
        self._conn.set_character_set('utf8')

    def _is_conn_vaild(self):
        if self._conn:
            try:
                self._conn.ping()
                return True
            except BaseException:
                self._conn.close()
                self._conn = None
        return False


class MysqlExecutor:

    def __init__(self, conn_mgr):
        self._conn_mgr = conn_mgr

    def query(self, sql, how=0):
        """
        Return rows tuple.

        A row is formatted according to how:
        0 -- tuple (default)
        1 -- dictionary, key=column or table.column if duplicated
        2 -- dictionary, key=table.column
        """
        assert sql.upper().startswith("SELECT")
        conn = self._conn_mgr.get_connection()
        conn.query(sql)
        mysql_result = conn.store_result()
        return mysql_result.fetch_row(mysql_result.num_rows(), how)

    def call_procedure(self, sql, how):
        conn = self._conn_mgr.get_connection()
        conn.query(sql)
        mysql_result = conn.store_result()
        return mysql_result.fetch_row(mysql_result.num_rows(), how)

    def query_async(self, sql, record_handler, how=0, chunk_size=1024):
        """
        Note: Don't throw any exception in record_handler.
              Don't use the same connecton as this executor to query in
              the record_handler.
        """
        conn = self._conn_mgr.get_connection()
        assert sql.upper().startswith("SELECT")
        conn.query(sql)
        mysql_result = conn.use_result()
        while True:
            records = mysql_result.fetch_row(chunk_size, how)
            if not records:
                break
            else:
                for record in records:
                    record_handler(record)

    def execute(self, sql):
        """
        Return the affected rows count.
        """
        conn = self._conn_mgr.get_connection()
        assert not sql.upper().startswith("SELECT")
        conn.query(sql)
        return conn.affected_rows()


def get_executor(host, port, db, usr, pwd):
    return MysqlExecutor(MysqlConnManager(host, port, db, usr, pwd))


def escape(sql):
    sql = str(sql)
    if not sql:
        return ""
    if isinstance(sql, unicode):
        sql = sql.encode('utf8')
    return _mysql.escape_string(sql)


def get_mysql_cond(cond_dict):
    if not cond_dict:
        return ""

    condstr = "WHERE"
    for k, v in cond_dict.items():
        condstr += " `%s`='%s' AND" % (k, escape(v))
    if condstr:
        condstr = condstr[:-3]
    return condstr
