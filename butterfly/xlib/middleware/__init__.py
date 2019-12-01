# coding=utf8

import logging

from xlib.db import  my_database
from xlib.util import wrapt
from xlib import auth

@wrapt.decorator
def db_close(wrapped, instance, args, kwargs):
    result = wrapped(*args,**kwargs)
    if not my_database.is_closed():
        my_database.close()
    return result

@wrapt.decorator
def login_required(wrapped, instance, args, kwargs):
    """
    使用 web 接口访问时，是通过 kwargs 进行传值
    使用 test_handler.py 进行接口调试时，则是使用 args 进行传值，所以接口调试时会自动绕过身份验证
    """
    if "req" in kwargs:
        req = kwargs["req"]
        log_msg = "[reqid]:{reqid} [wsgienv]:{wsgienv}".format(reqid=req.reqid,wsgienv=str(req.wsgienv))
        logging.info(log_msg)
        token_check = auth.is_token_valid(req)
        if not token_check.success:
            return token_check.err_content
        else:
            req.username = token_check.token_info["username"]
    result = wrapped(*args,**kwargs)
    return result
