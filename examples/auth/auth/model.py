#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-11-13 23:26:06

# File Name: model.py
# Description:

"""

from datetime import datetime

from xlib.db import BaseModel
from xlib.db.peewee import PrimaryKeyField
from xlib.db.peewee import CharField
from xlib.db.peewee import DateTimeField


class User(BaseModel):
    # If none of the fields are initialized with primary_key=True,
    # an auto-incrementing primary key will automatically be created and named 'id'.
    id = PrimaryKeyField()
    email = CharField(index=True, max_length=64)
    username = CharField(unique=True, max_length=32)
    password = CharField(null=True, max_length=64)
    createTime = DateTimeField(column_name="create_time", default=datetime.now)
    class Meta:
        table_name = 'tb_user'
        # If Models without a Primary Key
        # primary_key = False

    def __str__(self):
        return "User(id：{} email：{} username：{} password：{} createTime: {})".format(self.id, self.email, self.username, self.password, self.createTime)

def create_user(email="meetbill@163.com",username="meetbill",password="meet"):
    # 创建 User 对象
    user = User.create(email=email, username=username, password=password)
    # 保存 User
    print user.save()

def create_table():
    from xlib.db import my_database
    if not my_database.table_exists([User]):
        my_database.create_tables([User])

def drop_tables():
    from xlib.db import my_database
    if my_database.table_exists([User]):
        my_database.drop_tables([User])

if __name__ == "__main__":
    import sys, inspect
    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                          str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
        except Exception, e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
