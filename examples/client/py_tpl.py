#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-06-17 22:14:42

# File Name: py_tpl.py
# Description:

"""
import urllib2

request = urllib2.Request("http://127.0.0.1:8585/ping")
#request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
response = urllib2.urlopen(request)
# 返回码
print "ret_code:",response.getcode()
print "url:",response.geturl()
# 返回内容
print "content:",response.read()
# 请求id，此 id 会打印到 butterfly 日志中
print "x-reqid:",response.info().getheader('x-reqid')
# 请求耗时
print "x-cost:",response.info().getheader('x-cost')
