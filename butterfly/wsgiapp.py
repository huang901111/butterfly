# coding:utf8

from xlib import httpgateway
from xlib import protocol_json
from xlib import retstat

import apidemo

from conf import logger_conf
from conf import config
import inspect

apicube = {}


def addapi(name, func, is_parse_post, is_encode_response):
    """注册函数
    Args:
        name: 函数的注册名，默认为包中函数的全小写方法名
        func：函数
        is_parse_post: 是否支持 post 请求
        is_encode_response: 是否 encode 为 utf8
    """
    apicube[name] = protocol_json.Protocol(func, retstat.ERR_SERVER_EXCEPTION, retstat.ERR_BAD_PARAMS,
                                           is_parse_post, is_encode_response, logger_conf.errlog)


def add_apis(module, api_adder, adder_args):
    for func_name, func in module.__dict__.iteritems():
        if func_name.startswith("_"):
            continue
        if not inspect.isfunction(func):
            continue
        args_count = func.func_code.co_argcount
        if args_count < 1:
            continue
        args = func.func_code.co_varnames
        if args[0] != "req":
            continue
        print func_name
        api_adder(func_name.lower(), func, *adder_args)

# 将 apidemo module 中的函数进行注册
add_apis(apidemo, addapi, [True, True])
#addapi("ping", apidemo.ping, True, True)

# 用于处理 application 中 environ
wsgigw = httpgateway.WSGIGateway(
    httpgateway.get_func_name,
    logger_conf.errlog,
    logger_conf.acclog,
    apicube,
    config.STATIC_PATH,
    config.STATIC_PREFIX
    )


def application(environ, start_response):
    try:
        status, headders, content = wsgigw.process(environ)
        start_response(status, headders)
        return content
    except BaseException:
        start_response("500 Internal Server Error", [("GateWayError", "UnknownException")])
        return ()


if __name__ == '__main__':
    from xlib import logger as _logger
    _logger.set_debug_verbose()

    import sys
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    print "[Debug][Single-Threaded] HTTP listening on 0.0.0.0:%s..." % port
    from wsgiref.simple_server import make_server

    httpd = make_server('', port, application)
    httpd.serve_forever()
