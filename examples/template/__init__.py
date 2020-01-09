#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-07-21 09:31:43

# File Name: template
# Description:
    模板 demo
"""
__info__ = "meetbill"
__version__ = "1.0.1"

from xlib.httpgateway import Request
from xlib import retstat
from xlib import template


def helloworld(req):
    """
    使用 butterfly 模板
    eg(output):
        Hello, world! name: meetbill age : 21
    """
    isinstance(req, Request)
    text_src = '''
    Hello, {{name}}!

    name: {{user.name}}
    age : {{user.age}}
    '''
    tpl_dict = {"name": "world", "user": {"name": "meetbill", "age": 21}}

    t = template.Templite(text_src)
    text = t.render(tpl_dict)
    # => Hello, world!
    return retstat.HTTP_OK, text, [("Content-Type", "text/html")]


def demo_for(req):
    """
    for 循环 demo

    注意：
        {{name|upper}} 间不能有空格
    eg(output):
        Hello MEETBILL!
        You are interested in Python.
        You are interested in Geometry.
        You are interested in Juggling.
    """
    isinstance(req, Request)

    text_src = '''
            <h1>Hello {{ name|upper}}!</h1>
            {% for topic in topics %}
                <p>You are interested in {{topic}}.</p>
            {% endfor %}
    '''
    rule_dict = {'upper': str.upper}
    t = template.Templite(text_src, rule_dict)
    tpl_dict = {'name': "meetbill", 'topics': ['Python', 'Geometry', 'Juggling']}
    text = t.render(tpl_dict)
    return retstat.HTTP_OK, text, [("Content-Type", "text/html")]


def demo_if(req):
    """
    条件语句 demo

    eg(output):
        Hello MEETBILL!
        show OK
    """
    isinstance(req, Request)

    text_src = '''
            <h1>Hello {{ name|upper}}!</h1>
            {% if var %} show OK {% endif %}
    '''
    rule_dict = {'upper': str.upper}
    t = template.Templite(text_src, rule_dict)
    tpl_dict = {'name': "meetbill", 'var': True}
    text = t.render(tpl_dict)
    return retstat.HTTP_OK, text, [("Content-Type", "text/html")]
