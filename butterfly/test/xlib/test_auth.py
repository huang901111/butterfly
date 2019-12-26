#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-08-09 15:07:57

# File Name: test_auth.py
# Description:

"""
from xlib import auth
from xlib import httpgateway

def test_auth():
    token = auth.gen_token("meetbill")

    # OK
    reqid="ceshi"
    ip = "127.0.0.1"
    wsgienv = {
            "HTTP_AUTHORIZATION":"Bearer: {}".format(token)
            }
    req = httpgateway.Request(reqid, wsgienv, ip)
    token_status = auth.is_token_valid(req)
    assert token_status.success == True

    # ERR: You are not authorized
    wsgienv = {
            "HTTP_NOAUTH":"Bearer: {}".format(token)
            }
    req = httpgateway.Request(reqid, wsgienv, ip)
    token_status = auth.is_token_valid(req)
    assert token_status.success == False
    assert token_status.err_content == (401,{'message': 'You are not authorized: Not found token', 'success': False})

    # ERR: You are not authorized
    wsgienv = {
            "HTTP_AUTHORIZATION":"Bearer: xxxx"
            }
    req = httpgateway.Request(reqid, wsgienv, ip)
    token_status = auth.is_token_valid(req)
    assert token_status.success == False
    assert token_status.err_content == (401,{'message': 'You are not authorized: Failed to decode token', 'success': False})

    # ERR: Token has expired
    auth.JwtManager.init(secret="meetbill")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJidXR0ZXJmbHkiLCJpYXQiOjE1NjUzMDcwMTcsInVzZXJuYW1lIjoibWVldGJpbGwiLCJqdGkiOiI0NTZjNDk4OC01YTJkLTQwYWUtODhmOC02NTA1YmQwM2U0NGEiLCJleHAiOjE1NjUzMzU4MTd9.tmTJ4InC9UXwg-0fErEdkoI33vVm6EHt2BNzydd2UmY"
    wsgienv = {
            "HTTP_AUTHORIZATION":"Bearer: {}".format(token)
            }
    req = httpgateway.Request(reqid, wsgienv, ip)
    token_status = auth.is_token_valid(req)
    assert token_status.success == False
    assert token_status.err_content == (401,{'message': 'You are not authorized: Token has expired', 'success': False})
