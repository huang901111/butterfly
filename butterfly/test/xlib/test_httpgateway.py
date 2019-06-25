#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-03-03 22:59:41

# File Name: test_httpgateway.py
# Description:

"""
from xlib import httpgateway

def test_get_func_name():
    """
    根据 URL PATH 获取函数名
    """
    wsgienv_1={"PATH_INFO":"/echo"}
    wsgienv_2={"PATH_INFO":"/echo/"}
    wsgienv_3={"PATH_INFO":"/echo/ceshi"}
    wsgienv_4={"PATH_INFO":"/echo/ceshi/"}
    # True
    assert httpgateway.get_func_name(wsgienv_1) == "echo"
    assert httpgateway.get_func_name(wsgienv_2) == "echo"
    # False
    assert httpgateway.get_func_name(wsgienv_3) != "echo"
    assert httpgateway.get_func_name(wsgienv_4) != "echo"
