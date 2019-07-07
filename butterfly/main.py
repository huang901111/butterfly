import resource
import signal

from xlib.cherrypy_wsgiserver import CherryPyWSGIServer

import wsgiapp
from conf import config

if __name__ == '__main__':
    server = CherryPyWSGIServer(
        config.SERVER_LISTEN_ADDR,
        wsgiapp.application,
        config.SERVER_THREAD_NUM,
        perfork=1)
    server.start()
