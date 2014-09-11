from marshal import json_marshal, simple_marshal

Ok = "Ok"
NotAllowed = "NotAllowed"
NotFound = 'NotFound'


def find_all_options(candidates, options):
    for option in options:
        for k, v in candidates:
            if k == option:
                yield v


def find_first_option(candidates, options):
    try:
        return next( find_all_options(candidates, options) )
    except StopIteration:
        return None


def marshal(obj, types=['simple']):
    if obj in (Ok, NotFound, NotAllowed):
        return obj
    return obj.marshal(types)


class RestValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super(Exception, self).__init__("Error setting resource: %s" % " | ".join(["%s: %s" % err for err in errors]))


class Rest(object):
    marshals = []
    auditors = []
    actions = []
    validators = []
    fields = []

    def __init__(object):
        pass

    def __call__(self, method, path=''):
        pass

    def marshal(self, types):
        pass

    def audit(self):
        pass

    def validate(self, value):
        pass

    def update(self, value):
        value = self.validate(value)
        super(RestType, self).update(value)

    def simple(self):
        pass

    def fields(self):
        pass


class RestObject(object):
    marshallers = [
        ('json', json_marshal),
        ('simple', simple_marshal)
    ]
    auditors = {}
    processors = {}
    fields = []

    def __init__(self, **args):
        self.set(args)

    def marshal(self, types):
        marshaller = find_first_option(self.marshallers, types)
        if marshaller:
            return marshaller(self)
        return None

    def audit(self, request):
        for fn in find_all_options(self.auditors, [request.method, '*']):
            response = fn(self)
            if response:
                return response

    def process(self, request):
        for fn in find_all_options(self.processors, [request.method, '*']):
            response = fn(self)
            if response:
                return response

    def set(self, value):
        errors = {}
        processed = {}
        for k, field in self.fields:
            try:
                processed[k] = field(value[k])
            except Exception, e:
                errors[k] = e
        if not errors:
            self.__dict__.update(processed)
        return errors

    def get(self):
        value = dict((k, self.__dict__[k]) for k, v in self.fields)
        value['_type'] = self._type

    def __call__(self):
        self.audit(request)
        self.process(request)
        return self


class RestInterface(object):
    def __init__(self, **types):
        self.types = {}
        self.types.update(types)
        self.map = {}

    def call(self, method, path, args=None):
        response = self.route(method, path, args)
        if response is None:
            return NotFound
        return response

    def route(self, method, path, args=None):
        if method == 'put':
            obj = self.put(path, args)
            return obj
        elif method == 'get':
            obj = self.get(path)
            return obj
        elif method == 'post':
            obj = self.get(path)
            return obj('/')
        elif method == 'delete':
            del self.map[url]
            return Ok
        else:
            return NotAllowed

    def put(self, url, obj):
        obj = self.objectify(obj)
        self.map[url] = obj
        return obj

    def get(self, url):
        return self.map.get(url, None)

    def objectify(self, args):
        if isinstance(args, RestObject):
            return args
        type = self.types[args['_type']]
        return type(**args)

    def add_type(self, name, type):
        self.types[name] = type


