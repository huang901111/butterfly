#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-06-25 09:59:08

# File Name: upload.py
# Description:

"""
from xlib.httpgateway import Request
from xlib import retstat
from xlib import httpgateway
import hashlib
import binascii


__info__ = "meetbill"
__version__ = "1.0.2"


def put(req, md5=""):
    """ upload file
    Args:
        md5:(string) File md5
    """
    isinstance(req, Request)
    req.start_timming()

    blkdata = httpgateway.read_wsgi_post(req.wsgienv)
    blksize = len(blkdata)
    req.timming("rp")
    if blksize < 1:
        return retstat.ERR_BAD_PARAMS

    blkmd5_digest = hashlib.md5(blkdata).digest()
    if md5 and md5 != binascii.b2a_hex(blkmd5_digest):
        return retstat.ERR_BLOCK_CRC_VERIFY_FAILED
    req.timming("md5")

    with open('/tmp/file_tmp', 'wb') as f:
        f.write(blkdata)

    fid = "xxxx"
    req.log_params["fid"] = fid
    return retstat.OK, {"fid": fid}
