#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-07-18 21:15:03

# File Name: test_httpgateway_app.py
# Description:

"""
def test_demo_test1(init_data):
    """
    test func demo_test1
    """
    # ERR_BAD_PARAMS
    environ={
            "PATH_INFO":"/demo_test1",
            "REMOTE_ADDR": "192.10.10.10"
            }
    status, headders, content = init_data.process(environ)
    assert status == "200 OK"
    assert content == ('{"stat": "ERR_BAD_PARAMS"}',)

    environ={
            "PATH_INFO":"/demo_test1",
            "REMOTE_ADDR": "192.10.10.10",
            "QUERY_STRING": "str_info1=meetbill"
            }
    status, headders, content = init_data.process(environ)
    assert status == "200 OK"
    ## headders : [('Content-Length', '26'), ('x-reqid', 'B820746074ACC4AF'), ('x-cost', '0.000111'), ('x-reason', 'Param check failed')]
    for headder in headders:
        if headder[0] == 'x-reason':
            assert headder[1] == "Param check failed"
    assert content == ('{"stat": "ERR_BAD_PARAMS"}',)

    # OK
    environ={
            "PATH_INFO":"/demo_test1",
            "REMOTE_ADDR": "192.10.10.10",
            "QUERY_STRING": "str_info=meetbill"
            }
    status, headders, content = init_data.process(environ)
    assert status == "200 OK"
    ## headders:[('Content-Length', '38'), ('x-reqid', '32E6F4F44155B85F'), ('x-cost', '0.000206')]
    assert len(headders) == 3
    assert content == ('{"stat": "OK", "str_info": "meetbill"}',)

def test_400(init_data):
    """
    not found api
    """
    # ERR_BAD_PARAMS
    environ={
            "PATH_INFO":"/demo_401",
            "REMOTE_ADDR": "192.10.10.10"
            }
    status, headders, content = init_data.process(environ)
    assert status == "400 Bad Request"
    ## headders:[('x-reqid', '83CAEEF6E4C397B7'), ('x-cost', '0.000029'), ('x-reason', 'API Not Found')]
    for headder in headders:
        if headder[0] == 'x-reason':
            assert headder[1] == "API Not Found"
    assert content == ""
