import json
from pprint import pprint
from fixtures import *

OZYMANDIAS = """
I met a traveller from an antique land
Who said: "Two vast and trunkless legs of stone
Stand in the desert. Near them, on the sand,
Half sunk, a shattered visage lies, whose frown,
And wrinkled lip, and sneer of cold command,
Tell that its sculptor well those passions read
Which yet survive, stamped on these lifeless things,
The hand that mocked them and the heart that fed:
And on the pedestal these words appear:
'My name is Ozymandias, king of kings:
Look on my works, ye Mighty, and despair!'
Nothing beside remains. Round the decay
Of that colossal wreck, boundless and bare
The lone and level sands stretch far away.
""".lstrip()


def test_resource(app):
    with app.test_client() as c:
        rv = c.get('/', headers={'Accept': 'text/json'})
        assert rv.status_code == 200
        assert rv.content_type.split(';')[0] == 'text/json'
        assert json.loads( rv.data )['name'] == 'Home'

        rv = c.get('/', headers={'Accept': 'text/html'})
        assert rv.status_code == 200
        assert rv.content_type.split(';')[0] == 'text/html'
        assert '<title>INDEX</title>' in rv.data


def DISABLED_test_accepts(app):
    with app.test_client() as c:
        rv = c.get('/', headers={'Accept': 'text/html; text/json'})
        assert rv.content_type.split(';')[0] == 'text/html'
        
        rv = c.get('/', headers={'Accept': 'text/json; text/html'})
        assert rv.content_type.split(';')[0] == 'text/json'


def test_collection(app, mongo):
    with app.test_client() as c:
        rv = c.post('/documents', headers={'Accept': 'text/json'}, data={
            'name': 'documents',
            'body': OZYMANDIAS
        })
        value = json.loads( rv.data )

        assert value['name'] == 'documents'
        assert value['body'] == OZYMANDIAS
        assert value['_version']

        rv = c.get('/documents/~history', headers={'Accept': 'text/json'})
        history = json.loads( rv.data )['contents']
        assert len(history) == 1
        assert history[0]['_id'] == value['_version']

        ozzyMANDIAS = OZYMANDIAS.replace('Ozymandias', 'Ozzy Osbourne')

        rv = c.post('/documents', headers={'Accept': 'text/json'}, data={
            'name': 'documents',
            'body': ozzyMANDIAS
        })
        value = json.loads( rv.data )

        assert value['name'] == 'documents'
        assert value['body'] == ozzyMANDIAS
        assert value['_version']
        
        rv = c.get('/documents/~history', headers={'Accept': 'text/json'})
        history = json.loads( rv.data )['contents']
        assert len(history) == 2
        assert set(x['data']['body'] for x in history) == set((OZYMANDIAS, ozzyMANDIAS))

        