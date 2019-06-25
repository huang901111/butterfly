#coding:utf8

import time
import base64
import os
import random
import urlparse
import socket
import traceback

def is_digit_vars(variables):
    for var in variables:
        if isinstance(var, str) and var.isdigit():
            continue
        elif isinstance(var, int):
            continue
        else:
            return False
    return True
            
def write_pid(path):
    open(path, "w").write(str(os.getpid()))
    
def nowstr():
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

class Base64_16:
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
    except:
        return 0

def is_ipv4(ipv4_str):
    try:
        fields = ipv4_str.split(".")
        if len(fields) != 4:
            return False
        for field in fields:
            if not field.isdigit():
                return False
        return True
    except:
        return False

def spliturl(url):
    assert url.startswith("http://")
    r = urlparse.urlsplit(url)
    host_port = r.netloc.split(":")
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 80
    path = r.path
    if r.query: path += ("?" + r.query)
    if r.fragment: path += ("#" + r.fragment)
    return host, port, path

__DOMAIN_TO_IP = {}
def dns_resolve(domain):
    global __DOMAIN_TO_IP
    if domain in __DOMAIN_TO_IP:
        return __DOMAIN_TO_IP[domain]
    
    try:
        ip = socket.gethostbyname(domain)
        __DOMAIN_TO_IP[domain] = ip
        return ip
    except:
        logger.errlog.log("Dns resolve error %s " % traceback.format_exc())
        return domain

def try_invoke(times, func_obj, errlog, log_str, **kwargs):
    for i in range(0, times):
        try:
            ret = func_obj(**kwargs)
            return ret
        except:
            errlog.log("%s tried=%s\n%s" % (log_str, i, traceback.format_exc()))
    return None

def httpget2dict(qs):
    if not qs:
        return {}
    else:
        queries = urlparse.parse_qs(qs)
        ret = {}
        for k, v in queries.items():
            k = str(k)
            if len(v) == 1:
                ret[k] = v[0]
            else:
                ret[k] = v
        return ret
