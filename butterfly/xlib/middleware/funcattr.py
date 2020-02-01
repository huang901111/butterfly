#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2020-02-01 15:23:59

# File Name: funcattr.py
# Description:

"""
def api(func):
    """
    common api
    """
    func.apiattr = {"is_parse_post": True, "is_encode_response": True}
    return func


def api_download(func):
    # default
    func.apiattr = {"is_parse_post": True, "is_encode_response": False}
    return func


def api_upload(func):
    func.apiattr = {"is_parse_post": False, "is_encode_response": True}
    return func
