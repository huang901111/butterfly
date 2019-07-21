#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-07-21 09:31:43

# File Name: face.py
# Description:

"""
__info__ = "meetbill"
__version__ = "1.0.1"

from xlib.httpgateway import Request
from xlib import retstat
from xlib import template
def main(req):
    """
    不使用模板，使用 AngularJS 框架
    """
    isinstance(req, Request)
    with open("./templates/index.html") as  f:
        context = f.read()
    return retstat.HTTP_OK, context,[("Content-Type","text/html")]
def tpl(req):
    """
    使用 butterfly 模板
    """
    isinstance(req, Request)
    text_src= "<h1>hello {{name}}</h1>"
    tpl_dict = {}
    tpl_dict["name"] = "meetbill"
    t = template.Templite(text_src,tpl_dict)
    text = t.render()
    return retstat.HTTP_OK, text,[("Content-Type","text/html")]
