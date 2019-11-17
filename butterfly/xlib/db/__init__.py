try:
    from urlparse import parse_qsl, unquote, urlparse
except ImportError:
    from urllib.parse import parse_qsl, unquote, urlparse

#from peewee import *
import peewee
from pool import PooledMySQLDatabase
from conf import config


schemes = {
    'mysql': peewee.MySQLDatabase,
    'mysql+pool': PooledMySQLDatabase,
    'postgres': peewee.PostgresqlDatabase,
    'postgresql': peewee.PostgresqlDatabase,
    'sqlite': peewee.SqliteDatabase,
}

def _parseresult_to_dict(parsed, unquote_password=False):

    # urlparse in python 2.6 is broken so query will be empty and instead
    # appended to path complete with '?'
    path_parts = parsed.path[1:].split('?')
    try:
        query = path_parts[1]
    except IndexError:
        query = parsed.query

    connect_kwargs = {'database': path_parts[0]}
    if parsed.username:
        connect_kwargs['user'] = parsed.username
    if parsed.password:
        connect_kwargs['password'] = parsed.password
        if unquote_password:
            connect_kwargs['password'] = unquote(connect_kwargs['password'])
    if parsed.hostname:
        connect_kwargs['host'] = parsed.hostname
    if parsed.port:
        connect_kwargs['port'] = parsed.port

    # Adjust parameters for MySQL.
    if parsed.scheme == 'mysql' and 'password' in connect_kwargs:
        connect_kwargs['passwd'] = connect_kwargs.pop('password')
    elif 'sqlite' in parsed.scheme and not connect_kwargs['database']:
        connect_kwargs['database'] = ':memory:'

    # Get additional connection args from the query string
    qs_args = parse_qsl(query, keep_blank_values=True)
    for key, value in qs_args:
        if value.lower() == 'false':
            value = False
        elif value.lower() == 'true':
            value = True
        elif value.isdigit():
            value = int(value)
        elif '.' in value and all(p.isdigit() for p in value.split('.', 1)):
            try:
                value = float(value)
            except ValueError:
                pass
        elif value.lower() in ('null', 'none'):
            value = None

        connect_kwargs[key] = value

    return connect_kwargs

def connect(url, unquote_password=False, **connect_params):
    parsed = urlparse(url)
    connect_kwargs = _parseresult_to_dict(parsed, unquote_password)
    connect_kwargs.update(connect_params)
    database_class = schemes.get(parsed.scheme)

    if database_class is None:
        if database_class in schemes:
            raise RuntimeError('Attempted to use "%s" but a required library '
                               'could not be imported.' % parsed.scheme)
        else:
            raise RuntimeError('Unrecognized or unsupported scheme: "%s".' %
                               parsed.scheme)

    return database_class(**connect_kwargs)


my_database = connect(url=config.mysql_config_url)

class BaseModel(peewee.Model):
    """Common base model"""
    class Meta:
        database = my_database

if __name__ == "__main__":
    mysql_config_url="mysql+pool://root:password@127.0.0.1:3306/test?max_connections=300&stale_timeout=300"
    parsed = urlparse(mysql_config_url)
    """_parseresult_to_dict(parsed)
    {
        'database': 'test',
        'host': '127.0.0.1',
        'user': 'root',
        'stale_timeout': 300,
        'password': 'password',
        'port': 3306,
        'max_connections': 300
    }
    """
    print _parseresult_to_dict(parsed)

