from utils import to_json, from_json
from datetime import datetime as dt

from flask import render_template, current_app, request
from resource import Resource, BadRequest

from data import redis, mongo, ObjectId


class Collection(Resource):
    template = "index.html"

    def contents(self):
        return []

    def to_simple(self):
        simple = super(Collection, self).to_simple()
        simple['contents'] = self.contents()
        return simple


class TemplateCollection(Resource):
    def __init__(self, base='', **args):
        self.base = base.split('/')
        super(TemplateCollection, self).__init__(**args)

    def get(self, path):
        return render_template("/".join(self.base + path), resource=self)


class TemplateSourceCollection(TemplateCollection):
    def get(self, path):
        source, _, _ = current_app.jinja_env.loader.get_source(self, "/".join(self.base + path))
        return TemplateSourceResource(source=source)


class TemplateSourceResource(Resource):
    provide = ['text/plain']

    def to_text(self):
        return self.source


class MongoCollection(Collection):
    allow = ['get', 'post', 'delete']

    def __init__(self, *a, **kw):
        super(MongoCollection, self).__init__(*a, **kw)
        self.collection = getattr(mongo.db, self.name)

    def contents(self):
        results = self.collection.find()
        return [self.filter_result( x ) for x in results]

    def filter_result(self, result):
        obj = dict( result )
        obj['_id'] = str(obj['_id'])
        return obj

    def post(self, path):
        self.collection.insert( dict(request.form.items()) )
        return self

    def delete(self, path):
        if len(path) != 1:
            raise BadRequest()
        id = ObjectId(path[0])
        self.collection.remove(id, w=1)
        return self




class VersionHistory(Collection):
    def log(self, action, data):
        parent = self.get_version() or None
        #mongo.db.history.remove(); parent = None
        prev = self.replay()
        data = self.get_delta(prev, data)
        if not data:
            return
        delta = {
            'uri': self.target,
            'action': action,
            'data': data,
            'parent': ObjectId(parent) if parent else None,
            'utc': dt.utcnow()
        }
        mongo.db.history.insert( delta )
        redis.set("history:version:%s" % self.target, str( delta['_id'] ))
        print delta
        redis.publish('history', to_json(delta))

    def get_version(self):
        return redis.get("history:version:%s" % self.target)

    def contents(self):
        return list( mongo.db.history.find({'uri': self.target}).sort([('when', pymongo.DESCENDING)]) )

    def get_delta(self, prev, next):
        delta = {}
        for k, v in next.items():
            if prev.get(k) != next.get(k):
                delta[k] = v
        return delta

    def get_delta_list(self):
        changes = list( mongo.db.history.find({'uri': self.target}) )
        if not changes:
            return []
        by_parent = dict((delta['parent'], delta) for delta in changes)
        order = [by_parent.pop(None)]
        while True:
            top = order[-1]
            next = by_parent.get(top['parent'])
            print next
            if not next:
                break
            order.append(next)
        return order

    def replay(self):
        result = {}
        for delta in self.get_delta_list():
            self.apply_delta(result, delta)
        return result

    def apply_delta(self, obj, delta):
        for k, v in delta['data'].items():
            obj[k] = v

    @classmethod
    def setup(self):
        pass



class DocumentCollection(Collection):
    template = "document.html"
    allow = ['get', 'post', 'delete']

    def __init__(self, *a, **kw):
        super(DocumentCollection, self).__init__(*a, **kw)
        self.history = VersionHistory(uri='%s/~history' % self.uri, target=self.uri)

    def get(self, path):
        if path == ['~history']:
            return self.history
        src = redis.get(self.uri)
        if src:
            self.value = from_json(src)
            return self
        else:
            return None

    def post(self, path):
        self.value = dict( request.form.items() )
        redis.set(self.uri, to_json(self.value))
        self.history.log('update', self.value)
        return self

    def to_simple(self):
        self.value['_version'] = self.history.get_version()
        return self.value


