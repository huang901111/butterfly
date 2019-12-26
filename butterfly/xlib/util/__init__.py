# coding:utf8
"""
Butterfly 工具 module
"""

import time
import os
import urlparse


def is_digit_vars(variables):
    """
    Check if the variable is a number
    """
    for var in variables:
        if isinstance(var, str) and var.isdigit():
            continue
        elif isinstance(var, int):
            continue
        else:
            return False
    return True


def write_pid(path):
    """
    Write PID
    """
    open(path, "w").write(str(os.getpid()))


# ********************************************************
# * Time lib                                             *
# * https://www.runoob.com/python/python-date-time.html  *
# ********************************************************
def nowstr():
    """
    返回字符串格式的当前时间

    Example:
        '2019-12-26 22:22:52'
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_internet_tm(s):
    """
    Args:
        s: 时间字符串('Thu, 26 Dec 2019 22:27:14 GMT')
    Returns:
        时间戳
    # time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.localtime()) ==> 'Thu, 26 Dec 2019 22:27:14 GMT'
    # time.strptime("Thu, 26 Dec 2019 22:27:14 GMT", "%a, %d %b %Y %H:%M:%S GMT") 
    # time.struct_time(tm_year=2019, tm_mon=12, tm_mday=26, tm_hour=22, tm_min=27, tm_sec=14, tm_wday=3, tm_yday=360, tm_isdst=-1)
    """
    return time.mktime(time.strptime(s, "%a, %d %b %Y %H:%M:%S GMT"))


def mk_internet_tm(t):
    """
    Args:
        时间戳
    Returns:
        字符串

    # time.gmtime([secs])  接收时间戳（1970纪元后经过的浮点秒数）并返回格林威治天文时间下的时间元组t。
    """
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(t))


def spliturl(url):
    """
    拆分 url

    Args:
        url：HTTP url
    Returns:
        (host,port,path)
    """
    assert url.startswith("http://")
    r = urlparse.urlsplit(url)
    host_port = r.netloc.split(":")
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 80
    path = r.path
    if r.query:
        path += ("?" + r.query)
    if r.fragment:
        path += ("#" + r.fragment)
    return host, port, path
