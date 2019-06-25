#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-03-03 21:15:39

# File Name: server.py
# Description:

"""
# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('0.0.0.0', 8000, application)
print "Serving HTTP on port 8000..."
# 开始监听HTTP请求:
httpd.serve_forever()
