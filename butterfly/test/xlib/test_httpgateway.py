#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-03-03 22:59:41

# File Name: test_httpgateway.py
# Description:

"""
from xlib import httpgateway
def test_check_param():
    """
    check_param
    """
    params1 = {"param_a":"test","param_b":"test"}
    params2 = {"param_c":"test","param_b":"test"}
    params3 = {"param_a":"test"}
    params4 = {"param_a":"test","param_b":"test","param_c":"test"}
    def hello(param_a,param_b):
        print param_a,param_b
        pass
    # True
    assert httpgateway.check_param(hello,params1)
    # False
    assert httpgateway.check_param(hello,params2) == False
    assert httpgateway.check_param(hello,params3) == False
    assert httpgateway.check_param(hello,params4) == False

def test_read_wsgi_port():
    """test read_wsgi_port
    'wsgi.input': <socket._fileobject object at 0x7faa6d7a0e50> (Inconvenient testing)
    """
    wsgienv_1 = {"CONTENT_LENGTH":""}
    # True
    assert httpgateway.read_wsgi_post(wsgienv_1) == ""

def test_get_func_name():
    """
    根据 URL PATH 获取函数名
    """
    wsgienv_1={"PATH_INFO":"/echo"}
    wsgienv_2={"PATH_INFO":"/echo/"}
    wsgienv_3={"PATH_INFO":"/echo/ceshi"}
    wsgienv_4={"PATH_INFO":"/echo/ceshi/"}
    wsgienv_5={"PATH_INFO":"/"}
    # True
    assert httpgateway.get_func_name(wsgienv_1) == "/echo"
    assert httpgateway.get_func_name(wsgienv_2) == "/echo"
    assert httpgateway.get_func_name(wsgienv_3) == "/echo/ceshi"
    assert httpgateway.get_func_name(wsgienv_4) == "/echo/ceshi"
    assert httpgateway.get_func_name(wsgienv_5) == "/"
