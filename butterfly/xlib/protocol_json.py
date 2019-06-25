# coding:utf8
"""
# Author: meetbill
# Created Time : 2019-03-04 14:44:34

# File Name: protocol_json.py
# Description:
"""

import traceback
import json
import httplib
from collections import Iterable

from httpgateway import check_param
from httpgateway import httpget2dict
from httpgateway import read_wsgi_post


class Protocol(object):
    """Returns http Request
    Args:
        _func:(String) func name
        _errlog: err log
        _code_err: err code
        _code_badparam:
        _is_parse_post:_is_encode_response:
    """

    def __init__(self, func, code_err, code_badparam,
                 is_parse_post, is_encode_response, errlog):
        self._func = func
        self._errlog = errlog
        self._code_err = code_err
        self._code_badparam = code_badparam
        self._is_parse_post = is_parse_post
        self._is_encode_response = is_encode_response

    def _mk_ret(self, req, stat, data, headers):
        if data is None:
            data = {}
        if headers is None:
            headers = []
        try:
            jsoncontent = self._mk_json_content(stat, data)
        except BaseException:
            req.log(
                self._errlog,
                "Json dump failed\n%s" %
                traceback.format_exc())
            req.error_str = "Dump json exception"
            return "200 OK", [], ""
        headers.append(("Content-Length", str(len(jsoncontent))))
        return "200 OK", headers, (jsoncontent,)

    def _mk_json_content(self, stat, data):
        data["stat"] = stat
        ret = json.dumps(data)
        if isinstance(ret, unicode):
            ret = ret.encode("utf8")
        return ret

    def _mk_err_ret(self, req, is_bad_param, err_msg, log_msg):
        req.error_str = err_msg
        if log_msg:
            req.log(self._errlog, log_msg)

        if self._is_encode_response:
            err_code = self._code_badparam if is_bad_param else self._code_err
            req.log_ret_code = err_code
            return self._mk_ret(req, err_code, None, [])
        else:
            err_code = 400 if is_bad_param else 500
            req.log_ret_code = err_code
            status_line = "%s %s" % (
                err_code, httplib.responses.get(err_code, ""))
            return status_line, [], ""

    def __call__(self, req):
        try:
            params = httpget2dict(req.wsgienv.get("QUERY_STRING"))
            if self._is_parse_post and req.wsgienv.get(
                    "REQUEST_METHOD") == "POST":
                post_data = read_wsgi_post(req.wsgienv)
                if post_data:
                    post_params = json.loads(post_data)
                    for k, v in post_params.iteritems():
                        params[str(k)] = v
            req.log_params.update(params)

            params["req"] = req

            if not check_param(self._func, params):
                return self._mk_err_ret(
                    req, True, "Param check failed", "%s Param check failed" % req.ip)
        except BaseException:
            return self._mk_err_ret(req, True, "Param check exception", "%s Param check failed\n%s" % (
                req.ip, traceback.format_exc()))

        try:
            ret = self._func(**params)
            headers = []
            if self._is_encode_response:
                code = self._code_err
                data = {}
                if isinstance(ret, (str, int)):
                    code = ret
                elif len(ret) == 2:
                    code, data = ret
                elif len(ret) == 3:
                    code, data, headers = ret
                else:
                    return self._mk_err_ret(
                        req, False, "Invalid ret format", "Invalid ret format %s" % type(ret))

                req.log_ret_code = code
                return self._mk_ret(req, code, data, headers)
            else:
                status = 500
                data = ""
                if isinstance(ret, int):
                    status = ret
                elif len(ret) == 2:
                    status, data = ret
                elif len(ret) == 3:
                    status, data, headers = ret
                else:
                    return self._mk_err_ret(
                        req, False, "Invalid ret format", "Invalid ret format %s" % type(ret))

                if not isinstance(data, Iterable):
                    return self._mk_err_ret(
                        req, False, "Invalid ret format", "Invalid ret format, data %s" % type(data))
                elif not isinstance(status, int):
                    return self._mk_err_ret(
                        req, False, "Invalid ret format", "Invalid ret format, status %s" % type(status))

                req.log_ret_code = status
                status_line = "%s %s" % (
                    status, httplib.responses.get(status, ""))
                return status_line, headers, data
        except BaseException:
            return self._mk_err_ret(
                req, False, "API Processing Exception", "Server exception\n%s" % traceback.format_exc())
