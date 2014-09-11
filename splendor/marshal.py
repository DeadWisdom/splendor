import json

def json_marshal(obj):
    return json.dumps(obj.simple())

def simple_marshal(obj):
    return obj.get()