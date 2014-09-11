import json
from datetime import datetime, date
from flask import current_app, request
from data import ObjectId

class EnhancedJSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, 'simple'):
        return obj.simple()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return str(obj)
    return json.JSONEncoder.default(self, obj)


def render_json(obj):
    if request.is_xhr:
        indent = 0
    else:
        indent = 2
    src = json.dumps(obj, cls=EnhancedJSONEncoder, indent=indent)
    return current_app.response_class(src, mimetype='application/json')


def to_json(obj):
    return json.dumps(obj, cls=EnhancedJSONEncoder)

def from_json(src):
    return json.loads(src)


def accepts(*types):
    for t in types:
        if t in request.headers['Accept']:
            return True
    return False


def request_wants(types=['text/html', 'application/json', 'application/xml', 'text/plain']):
    for obj, quality in request.accept_mimetypes:
        if obj == '*/*':
            return '*/*'
        if obj in types:
            return obj
    return None


def generate_search_paths(path):
    """
    Generates 2-tuples for searching

    >>> list(generate_search_paths('/path/to/this'))
    [ 
        ('path/to/this', []),
        ('path/to', ['this']),
        ('path', ['to', 'this']),
        ('', ['path', 'to', 'this']) 
    ]

    >>> list(generate_search_paths('/path'))
    [ 
        ('path', []),
        ('', ['path']) 
    ]
    """
    left, right = list(path.split('/')), []
    while left:
        yield "/".join(left) or '/', right
        right.append(left.pop(-1))
    
