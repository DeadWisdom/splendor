def find_all_options(candidates, options):
    for option in options:
        for k, v in candidates:
            if k == option:
                yield v


def find_first_option(candidates, options):
    return find_all_options(candidates, options).next()

blue = Module('blue')

@blue.register
def post_object():
    pass

@blue



class RestInterface(object):
    def __init__(self):
        pass

    def get(self, url, context):
        pass

    def put(self, url, context):
        pass

    def post(self, url, context):
        pass

    def delete(self, url, context):
        pass



#### 

class RestObject(object):
    marshallers = []
    auditors = {}
    processors = {}

    def marshal(self, types):
        marshaller = find_first_option(self.marshallers, types)
        if marshaller:
            return marshaller(self)
        return None

    def audit(self):
        for fn in find_all_options(self.auditors, [request.method, '*']):
            response = fn(self)
            if response:
                return response

    def process(self, path):
        for fn in find_all_options(self.processors, [request.method, '*']):
            response = fn(self)
            if response:
                return response

    def __call__(self, path):
        self.audit()
        self.process()
        if path:
            return None
        return self



URL MAP -> {}
GET -> gets it

PUT -> 


ElasticSearch
Redis
MongoDB


####
rest = ()
while path:
    find object with uri == path
    if found:
        return object
    else:
        path, rest = path.rsplit('/', 1)

object(rest)

PUT site -> /
PUT tasks -> /tasks
PUT auth -> /auth
PUT sentry -> /sentry


