"""
Gevent SocketIO handling

gevent-socketio is made in a needlessly class-heavy way.  So this helps get around this sort of thing.

/splendor/socket/
"""

import os, logging

from flask import request, current_app
from gevent import monkey
from geventwebsocket.server import WebSocketServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication


logger = logging.getLogger('WebSocket')
logger.addHandler(logging.StreamHandler())


def get_address(host, port, default):
    if host is None:
        host = '127.0.0.1'
    if port is None:
        server_name = default
        if server_name and ':' in server_name:
            port = int(server_name.rsplit(':', 1)[1])
        else:
            port = 5000
    return (host, port)


def run(app, host=None, port=None, debug=None, logger=logger):
    monkey.patch_all()

    address = get_address(host, port, app.config['SERVER_NAME'])

    if debug is not None:
        app.debug = debug

    if app.debug:
        #app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
        server = WebSocketServer(address, app.wsgi_app, debug=debug)
        server._logger = logger

        logger.setLevel(logging.INFO)
        def run_server():
            server.serve_forever()
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            server.logger.info(' * Running on http://%s:%d/' % address)
            server.logger.info(' * WebSocket enabled')
        run_with_reloader(run_server)
    else:
        server = WebSocketServer(address, app.wsgi_app, debug=debug)
        server._logger = logger
        server.serve_forever()
    return server

def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            message = ws.wait()
            ws.send(message)


#import logging
#import inspect

#from flask import request, current_app
#from socketio.namespace import BaseNamespace
#from socketio.server import SocketIOServer
#from werkzeug.serving import run_with_reloader

#from utils import to_json, from_json


#logger = logging.getLogger('socketio.virtsocket')


#def get_address(host, port, default):
#    if host is None:
#        host = '127.0.0.1'
#    if port is None:
#        server_name = default
#        if server_name and ':' in server_name:
#            port = int(server_name.rsplit(':', 1)[1])
#        else:
#            port = 5000
#    return (host, port)


#class ResourceNamespace(BaseNamespace):



#class TriggerNamespace(BaseNamespace):
#    def __init__(self, *args, **kwargs):
#        super(TriggerNamespace, self).__init__(*args, **kwargs)
#        self.methods = {}

#    def call_method(self, method_name, packet, *args):
#        method = self.methods.get(method_name, None)
#        if method is None:
#            self.error('no_such_method',
#                       'The method "%s" was not found' % method_name)
#            return

#        specs = inspect.getargspec(method)
#        func_args = specs.args
#        if not len(func_args) or func_args[0] != 'self':
#            self.error("invalid_method_args",
#                "The server-side method is invalid, as it doesn't "
#                "have 'self' as its first argument")
#            return

#        # Check if we need to decorate to handle exceptions
#        if hasattr(self, 'exception_handler_decorator'):
#            method = self.exception_handler_decorator(method)

#        if len(func_args) == 2 and func_args[1] == 'packet':
#            return method(packet)
#        else:
#            return method(*args)


#def namespace_factory(cls=TriggerNamespace, **kwargs):
#    def creator():
#        return cls(**kwargs)
#    return creator


#class SocketIO(object):
#    def __init__(self, namespaces={}, resource='socket.io', default=namespace_factory(TriggerNamespace)):
#        self.resource = base
#        self.namespaces = {}
#        self.default = default
#        self.update(namespaces)

#    def update(self, namespaces):
#        self.namespaces.update(name)

#    def set(self, name, cls):
#        self.namespaces[name] = cls

#    def get(self, name):
#        return self.namespaces.get(name)

#    def bind(self, fn, name, namespace=''):
#        if namespace not in self.namespaces:
#            namespace = self.default()
#            self.set(namespace)

#    def on(self, name, namespaces=''):
#        def decorator(fn):
#            self.bind(fn, name, namespace)
#            return fn
#        return decorator

#    def run(self, app, host=None, port=None, **kwargs):
#        address = get_address(host, port, app.config['SERVER_NAME'])
#        kwargs.setdefault('resource', self.resource)
#        
#        server = SocketIOServer(address, app.wsgi_app, **kwargs)
#        if app.debug:
#            if not log.handlers:
#                log.addHandler(logging.StreamHandler())

#            def run_server():
#                server.serve_forever()
#            if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
#                _log('info', ' * Running on http://%s:%d/' % (host, port))
#                _log('info', ' * Socket IO Enabled')
#            run_with_reloader(run_server)
#        else:
#            server.serve_forever()

#        return server

#    def __call__(self):
#        if 'socketio' not in request.environ:
#            raise RuntimeError('You need to use a gevent-socketio server.')

#        request.socket = self

#        return socketio_manage(environ, self.namespaces, request,
#                                json_loads=from_json, json_dumps=to_json, **manage_kwargs)


