# coding:utf8

import uuid
import ctypes
import os
import base64
import pyDes


class UUID64(object):

    ENC_KEY = "ZDgxN2Q4"

    def __init__(self):
        self._pid = os.getpid()
        self._pid_factor = (self._pid & 0x0f) << 4
        self.counter = 0
        self._cipher = pyDes.des(self.ENC_KEY)

        if uuid._uuid_generate_time:
            buf = ctypes.create_string_buffer(16)
            uuid._uuid_generate_time(buf)
            raw = buf.raw
        else:
            raw = uuid.uuid1().get_bytes()
        self._host_id = raw[-2:]

    def gen(self):
        self.counter += 1

        if uuid._uuid_generate_time:
            buf = ctypes.create_string_buffer(16)
            uuid._uuid_generate_time(buf)
            raw = buf.raw
        else:
            raw = uuid.uuid1().get_bytes()

        tm = (raw[4] + raw[5]) + (raw[0] + raw[1]) + \
            chr((ord(raw[2]) & 0xf0) | (self.counter & 0x0f))
        mid = chr(self._pid_factor | (ord(raw[7]) & 0x0f))

        uuid64 = "%s%s%s" % (self._host_id, mid, tm)
        return base64.b16encode(self._cipher.encrypt(uuid64))
