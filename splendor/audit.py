

__audits = {}


def register_audit(name, fn):
    __audits[name] = fn


def get_audit(name):
    return __audits[name]


def perform_audit(name, resource):
    if name.startswith('!'):
        fn = get_audit(name[1:])
        return not fn(resource)
    else:
        fn = get_audit(name)
        return fn(resource)


def audit(name=None):
    if isinstance(name, basestring):
        def outer(fn):
            register_audit(name, fn)
            return fn
        return outer
    else:
        fn = name
        register_audit(fn.func_name, fn)
        return fn


### Stock Audits ###
from flask import current_app

@audit
def is_debug(resource):
    return current_app.debug
