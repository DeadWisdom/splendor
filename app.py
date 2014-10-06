#!env/bin/python
from flask import Flask
from flask.ext.assets import Environment
from splendor import Splendor
from splendor.ws import run


def create_app(config):
    """App factory for the splendor application."""

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

