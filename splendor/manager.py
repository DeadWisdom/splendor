from collection import Collection
from data import redis, mongo
from flask import request, current_app
from utils import to_json
from gevent import monkey
from geventwebsocket import WebSocketError

monkey.patch_all()



class Manager(Collection):
    template = "manager.html"

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        self.history = AdminHistory(self.uri + '/history', template=self.template)
        self.root = AppCollection(self.uri + '/history', template=self.template)
    
    def get(self, path):
        if path:
            if path[0] == 'history':
                return self.history('get', path[1:])
            if path[0] == 'root':
                return self.root('get', path[1:])
        return self
        #return render_template("admin.html", resource=self, **self.context)
    
    def contents(self):
        return list( current_app.splendor.iter_routes() )

    def socket(self, path):
        if path[0] == 'history':
            return self.history('socket', path[1:])
        if path[0] == 'root':
            return self.root('socket', path[1:])


class AdminHistory(Collection):
    def contents(self):
        return list( mongo.db.history.find() )

    def socket(self, path):
        ws = request.ws
        sub = redis.pubsub()
        sub.subscribe(['history'])
        for item in sub.listen():
            if ws.closed:
                return
            try:
                ws.send(unicode(item['data']))
            except WebSocketError:
                pass



class AppCollection(Collection):
    def contents(self):
        return sorted(list( current_app.splendor.iter_routes() ))

    def socket(self, path):
        ws = request.ws
        sub = redis.pubsub()
        sub.subscribe([':app'])
        for item in sub.listen():
            if ws.closed:
                return
            try:
                ws.send(unicode(item['data']))
            except WebSocketError:
                pass
