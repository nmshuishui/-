# coding: utf-8

from flask import session, redirect
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect('/login/')
        else:
            return func(*args, **kwargs)
    return wrapper
