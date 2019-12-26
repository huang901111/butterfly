# coding:utf8
"""
Butterfly 工具 module
"""

import time
import base64
import os
import random
import urlparse
import traceback


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
# ********************************************************
def nowstr():
    """
    返回字符串格式的当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_internet_tm(s):
    # http://tools.ietf.org/html/rfc2616.html#section-3.3
    return time.mktime(time.strptime(s, "%a, %d %b %Y %H:%M:%S GMT"))


def mk_internet_tm(t):
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(t))


def get_safevalue(cur, _min, _max):
    if cur < _min:
        return _min
    elif cur > _max:
        return _max
    else:
        return cur


class Base64_16(object):
    @staticmethod
    def b16_to_b64(b16str):
        if len(b16str) % 2 == 0:
            return base64.b64encode(base64.b16decode(b16str, True), "()").strip("=")
        else:
            return "@" + b16str[0] + base64.b64encode(base64.b16decode(b16str[1:], True), "()").strip("=")

    @staticmethod
    def b64_to_b16(b64str_v):
        if b64str_v[0] == "@":
            return b64str_v[1] + base64.b16encode(Base64_16.b64_to_bin(b64str_v[2:])).lower()
        else:
            return base64.b16encode(Base64_16.b64_to_bin(b64str_v)).lower()

    @staticmethod
    def b64_to_bin(b64str):
        slen = len(b64str)
        tail = slen % 4
        if tail:
            b64str += ("=" * (4 - tail))
        return base64.b64decode(b64str, "()")

    @staticmethod
    def bin_to_b64(b):
        return base64.b64encode(b, "()").strip("=")


def weighted_choice_sub(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

# ********************************************************
# * IP lib                                               *
# ********************************************************


def ipv4_to_int(ipv4_str):
    try:
        fields = ipv4_str.split(".")
        assert len(fields) == 4
        ip = 0
        for field in fields:
            field = int(field)
            assert field < 256
            ip = (ip << 8) | field
        return ip
    except BaseException:
        return 0


def is_ipv4(ipv4_str):
    """
    检查是否为 IP
    """
    try:
        fields = ipv4_str.split(".")
        if len(fields) != 4:
            return False
        for field in fields:
            if not field.isdigit():
                return False
        return True
    except BaseException:
        return False


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


def try_invoke(times, func_obj, errlog, log_str, **kwargs):
    for i in range(0, times):
        try:
            ret = func_obj(**kwargs)
            return ret
        except BaseException:
            errlog.log("%s tried=%s\n%s" % (log_str, i, traceback.format_exc()))
    return None
