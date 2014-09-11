#!env/bin/python

from flask import Flask
from flask.ext.assets import Environment
from splendor import Splendor
from splendor.ws import run


"""
    Splendor.follow(location.href)
    Splendor.on('update', ...)

    Splendor.stream({
        on: {
            connect: function() { ... },
            disconnect: function() { ... },
            error: function() { ... },
            update: function() { ... },
            more: function() { ... },
        },
        pause: {},
    });

    splendor.collection({
        on: {
            connect: function() { ... },
            disconnect: function() { ... },
            error: function() { ... },
            update: function() { ... },
            create: function() { ... },
            edit: function() { ... },
            delete: function() { ... },
            reorder: function() { ... },
        },
        create : function() { ... },
        edit : function() { ... },
        delete : function() { ... },
        reorder : function() { ... },
        move : function() { ... },

        send : function() { ... }
    });
    
    _super.fn_stack.pop();
            _super.context_stack.pop();

    myCollection = splendor.collection.extend({
        window._super = function() {

        }
    });

    splendor.on({
        connect: function() {},
        disconnect: function() {},
    });

    class Stream(Collection):
        pass

"""




def create_app(config):
    app = Flask(__name__)
    if isinstance(config, basestring):
        app.config.from_object(config)
    else:
        app.config.update(config)

    @app.route("/favicon.ico")
    def favicon():
        return ""
    
    assets = Environment(app)
    splendor = Splendor(app)

    splendor.clear()
    splendor.seed({
        '/': {
            'template': 'home.html',
            'context': {
                'name': 'Home',
            }
        },
        '/about': {
            'template': 'home.html',
            'context': {
                'name': 'About',
            }
        },
        '/templates': {
            'type': 'TemplateSourceCollection',
            'audits': ['is_debug']
        },
        '/people': {
            'type': 'MongoCollection',
            'name': 'people'
        },
        '/documents': {
            'type': 'DocumentCollection',
        },
        '/splendor': {
            'type': 'Manager',
        }
    })

    return app



if __name__ == '__main__':
    app = create_app('settings')
    #app.run(debug=True)
    run(app, debug=True)



