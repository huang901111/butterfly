from xlib.db import  my_database
from xlib.util import wrapt

@wrapt.decorator
def db_close(wrapped, instance, args, kwargs):
    result = wrapped(*args,**kwargs)
    if not my_database.is_closed():
        my_database.close()
    return result
