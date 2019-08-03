#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-08-02 21:14:43

# File Name: urls.py
# Description:
    Managing Routing and Automatically register the handler to route
"""

import importlib
import pkgutil
import inspect

from xlib import retstat
from xlib import protocol_json


def import_submodules(package):
    """
    Import all submodules of a module, recursively,
    including subpackages.

    From http://stackoverflow.com/questions/3365740/how-to-import-all-submodules

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]

    Examples:
        local dir:
            handlers/__init__.py
            handlers/api/__init__.py
        input: package = "handlers"
        return:{
                'handlers.api': <module 'handlers.api' from '/home/users/meetbill/butterfly/handlers/api/__init__.pyc'>,
                'handlers':     <module 'handlers' from '/home/users/meetbill/butterfly/handlers/__init__.pyc'>
               }
    """
    results = {}
    if isinstance(package, str):
        results[package] = importlib.import_module(package)
        package = importlib.import_module(package)
    for _loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        if is_pkg:
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
    return results


class Route(object):
    """Managing Route

    Attributes:
        infolog:(logger.LoggerBase) record info log
        errlog:(logger.LoggerBase) record error log
        apicube:(Dict) route info
    """

    def __init__(self, infolog, errlog):
        self._infolog = infolog
        self._errlog = errlog
        self.apicube = {}

    def addapi(self, name, func, is_parse_post, is_encode_response):
        """注册函数
        Args:
            name: 函数的注册名，默认为包中函数的全小写方法名
            func：函数
            is_parse_post: 是否将请求 Body 中的内容解析为参数，传递给后端 handler
            is_encode_response: 是否 encode 为 utf8
        """
        self.apicube[name] = protocol_json.Protocol(func, retstat.ERR_SERVER_EXCEPTION, retstat.ERR_BAD_PARAMS,
                                                    is_parse_post, is_encode_response, self._errlog)

    def add_apis(self, py_module, adder_args, package_name=""):
        """将某个 module 文件中函数注册到路由中
        Args:
            py_module:Python module or package
            adder_args:[is_parse_post,is_encode_response]
            package_name: If py_module is a package ,You have to pass this parameter.
        """
        for func_name, func in py_module.__dict__.iteritems():
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
            name = "{package_name}.{func_name}".format(
                package_name=package_name, func_name=func_name)
            # handlers.api.ping ==> /api/ping
            path_name = "/" + "/".join(name.split(".")[1:])
            self.addapi(path_name.lower(), func, *adder_args)
            args_count = func.func_code.co_argcount - 1 if inspect.ismethod(func) else func.func_code.co_argcount
            func_args = func.func_code.co_varnames[:args_count]
            self._infolog.log(
                    "[Init handler] {path:20} [args]:{func_args:30} [is_parse_post]:{is_parse_post} [is_encode_response]:{is_encode_response}".format(
                    path=path_name,
                    func_args=func_args,
                    is_parse_post=adder_args[0],
                    is_encode_response=adder_args[1]))

    def autoload_handler(self, package_dir):
        """自动加载指定目录下的所有 package
        Args:
            package_dir: package dir
        """
        # 将 "handlers" 目录下的 package 自动加载，也就是 __init__.py
        results = import_submodules(package_dir)
        for package_name in results:
            # 如果 package_name 是以 {package_dir}.api 开头，则说明为接口函数
            if package_name.startswith(
                    "{package_dir}.api".format(package_dir=package_dir)):
                adder_args = [True, True]
            else:
                adder_args = [False, False]
            self.add_apis(
                results[package_name],
                adder_args,
                package_name=package_name)

    def get_route(self):
        return self.apicube
