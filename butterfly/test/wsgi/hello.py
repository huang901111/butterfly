#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-03-03 21:15:59

# File Name: hello.py
# Description:

"""
def application(environ, start_response):
    print "[environ]:%s" % environ
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = 'Hello, WSGI!'
    # return result #python3 直接返回字符串会报错
    return [result.encode()] # 转成字节列表
