from utils import render_json, to_json
from flask import render_template, current_app, request
from audit import perform_audit
from geventwebsocket import WebSocketError

SHORT_TYPES = {
    'text/plain': 'text',
    'text/html': 'html',
    'application/xml': 'xml',
    'application/xhtml+xml': 'xhtml',
    'application/json': 'json',
    'text/json': 'json',
    'text/javascript': 'json',
    'application/javascript': 'json',
}


### Registration ###
__types = {}

def register_type(name, fn):
    __types[name] = fn

def get_type(name):
    return __types[name]

def resource_type(name=None):
    if isinstance(name, basestring):
        def outer(fn):
            register_type(name, fn)
            return fn
        return outer
    else:
        fn = name
        register_type(fn.func_name, fn)
        return fn


class ResourceMeta(type):
    def __init__(self, name, bases, attrs):
        super(ResourceMeta, self).__init__(name, bases, attrs)
        register_type(attrs.get('name', name), self)


### Resource Base ###
class Resource(object):
    __metaclass__ = ResourceMeta
    status_code = 200
    status = "OK"
    template = "resource.html"
    allow = ['get', 'head', 'post', 'put', 'patch', 'delete', 'socket']
    provide = ['text/html', 'text/json']
    audits = []
    context = {}
    headers = {}
    cookies = {}

    def __init__(self, uri, **props):
        self.uri = uri
        self.context = {}
        self.headers = {}
        self.cookies = {}
        self.__dict__.update(props)

    def __call__(self, method, path):
        method = method.lower()
        if method not in self.allow:
            return MethodNotAllowed(self.allow)
        if not self.audit(method, path):
            return Forbidden()
        fn = getattr(self, method, None)
        if not fn:
            return NotImplemented()
        return fn(path)

    def get(self, path):
        if path:
            raise NotFound()
        return self

    def head(self, path):
        if path:
            raise NotFound()
        return self

    def put(self, path):
        raise NotImplemented()

    def post(self, path):
        raise NotImplemented()

    def patch(self, path):
        raise NotImplemented()

    def delete(self, url):
        raise NotImplemented()

    def socket(self, path):
        raise NotImplemented()

    def audit(self, method, path):
        for name in self.audits:
            if not perform_audit(name, self):
                return False
        return True

    def marshal(self, *types):
        for mimetype in types:
            fn = getattr(self, 'to_%s' % SHORT_TYPES.get(mimetype, mimetype.replace('/', '_')), None)
            if fn:
                response = fn()
                if response:
                    return self.prepare_response(response, mimetype)
        return None

    def subscribe(self):
        pass

    def publish(self, object):
        pass

    def prepare_response(self, response, mimetype):
        response = current_app.make_response(response)
        response.status = self.status
        response.status_code = self.status_code
        response.headers.extend(self.headers)
        response.mimetype = mimetype
        for cookie in self.cookies:
            response.set_cookie(**cookie)
        return response

    def to_html(self):
        return render_template(self.template, resource=self, **self.context)

    def to_json(self):
        return render_json(self.to_simple())

    def to_simple(self):
        return self.context

    def setup(self, splendor):
        pass

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def tick(self):
        pass



### Exceptions ###
class HTTPException(BaseException, Resource):
    status_code = 0
    status = None
    template = "error.html"

    def __unicode__(self):
        return "Error %s: %s" % (self.status_code, self.status)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


### 3XX ##
class MovedPermanently(HTTPException):
    status_code = 403
    status = "Moved Permanently"

    def __unicode__(self):
        return "Redirection %s: %s" % (self.status_code, self.status)

class TemporaryRedirect(MovedPermanently):
    status_code = 307
    status = "Temporary Redirect"


### 4XX ##
class BadRequest(HTTPException):
    status_code = 400
    status = "Bad Request"

class Unauthorized(HTTPException):
    status_code = 401
    status = "Unauthorized"

class Forbidden(HTTPException):
    status_code = 403
    status = "Forbidden"

class NotFound(HTTPException):
    status_code = 404
    status = "Not Found"

class MethodNotAllowed(HTTPException):
    status_code = 405
    status = "Method Not Allowed"

    def __init__(self, allow, **context):
        super(MethodNotAllowed, self).__init__(**context)
        if not isinstance(allow, basestring):
            allow = ", ".join(x.upper() for x in sorted(allow))
        self.headers.update({'Allow': allow})


class NotAcceptable(HTTPException):
    """
    The resource identified by the request is only capable of generating response entities which have content 
    characteristics not acceptable according to the accept headers sent in the request.

    In other words, the client set an "Accept" header with mimetypes that we don't know how to give them.  All
    clients send an accept header, most of the web browsers end with '*/*' which basically means, give me
    whatever you got.

    See: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.7
    """
    status_code = 406
    status = "Not Acceptable"


### 5XX ##
class ServerError(HTTPException):
    status_code = 500
    status = "Server Error"

class NotImplemented(HTTPException):
    status_code = 501
    status = "Not Implemented"