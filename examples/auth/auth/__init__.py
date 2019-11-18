# coding=utf8
from xlib.httpgateway import Request
from xlib import retstat
from model import User
from xlib import middleware
from xlib.db import shortcuts
from xlib import auth

__info__ = "meetbill"
__version__ = "1.0.1"


@middleware.db_close
def login(req,username,password):
    isinstance(req,Request)
    try:
        user = User().select().where(User.username == username).get()
    except Exception as e:
        print e
        return retstat.HTTP_UNAUTHORIZED, {}, [(__info__, __version__)]
    if  shortcuts.model_to_dict(user)["password"] == password:
        result = {}
        token = auth.gen_token(username)
        token = token.decode("utf-8")
        result["token"] = token
        result["username"] =  username
        result["permissions"] = ""
        return retstat.HTTP_OK, result, [(__info__, __version__)]
    else:
        return retstat.HTTP_UNAUTHORIZED, {}, [(__info__, __version__)]
