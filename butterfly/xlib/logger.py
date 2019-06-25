# coding:utf8

import time
import traceback
import os

DEBUG_VERBOSE = False


def set_debug_verbose(v=True):
    global DEBUG_VERBOSE
    DEBUG_VERBOSE = v


class NullLogger:
    def __init__(self, **kwargs):
        pass

    def log(self, msg):
        pass


class EmptyLogger:
    def __init__(self, **kwargs):
        pass

    def log(self, msg):
        print msg


class LoggerBase:
    FILE_SIZE_CHECK_LINES = 1000

    def __init__(self, path, is_day_rolling, size_limit, batch_write):
        file_dir = os.path.dirname(path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        self._is_day_rolling = is_day_rolling
        self._size_limit = size_limit
        self._path = path
        self._batch_write = batch_write
        self._batches = []
        self._pid = os.getpid()

        self._curpath = ""
        self._tm = None
        self._writed_lines = 0
        self._fd = None

    def _reopen_file(self, mode):
        if self._fd is not None:
            os.close(self._fd)
        self._fd = os.open(self._curpath, mode, 0o644)

    def _checkfile(self, now):
        if self._is_day_rolling:
            if not self._tm or self._fd is None or now.tm_mday != self._tm.tm_mday:
                self._tm = now
                self._curpath = "%s%s" % (
                    self._path, time.strftime("%Y-%m-%d", self._tm))
                self._reopen_file(os.O_CREAT | os.O_APPEND | os.O_WRONLY)
        else:
            if self._fd is None:
                self._curpath = self._path
                self._reopen_file(os.O_CREAT | os.O_APPEND | os.O_WRONLY)

        if self._size_limit and self._writed_lines > self.FILE_SIZE_CHECK_LINES:
            if os.fstat(self._fd).st_size > self._size_limit:
                self._reopen_file(os.O_CREAT | os.O_APPEND |
                                  os.O_WRONLY | os.O_TRUNC)
                self._writed_lines = 0

    def log(self, logtype, info=""):
        now = time.localtime()
        self._checkfile(now)
        if info:
            logline = "%s\t%s\t%s\t%s" % (time.strftime(
                "%Y-%m-%d %H:%M:%S", now), self._pid, logtype, info)
        else:
            logline = "%s\t%s\t%s" % (time.strftime(
                "%Y-%m-%d %H:%M:%S", now), self._pid, logtype)
        if DEBUG_VERBOSE:
            print logline

        if self._batch_write < 2:
            os.write(self._fd, logline + "\n")
            self._writed_lines += 1
        else:
            self._batches.append(logline)
            if len(self._batches) >= self._batch_write:
                os.write(self._fd, "\n".join(self._batches) + "\n")
                self._writed_lines += len(self._batches)
                self._batches = []
