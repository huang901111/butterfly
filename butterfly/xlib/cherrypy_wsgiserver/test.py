
import __init__
import os

def simple_app(environ, start_response):
    response_headers = [('Content-type','text/plain')]
    start_response('200 OK', response_headers)
    return ['My Own Hello World!']

s = __init__.CherryPyWSGIServer(("localhost", 8080), simple_app, perfork=2)
s.start()
