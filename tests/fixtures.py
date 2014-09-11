import os
import pytest


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    from app import create_app
    from splendor.data import mongo, redis

    app = create_app({
        'TESTING': True,
        'MONGO_DBNAME': 'testing',
        'REDIS_DATABASE': 11
    })

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        redis.flushdb()
        mongo.cx.drop_database(app.config['MONGO_DBNAME'])
        ctx.pop()
        

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def mongo(request):
    from splendor.data import mongo
    return mongo


@pytest.fixture(scope='session')
def redis(request):
    from splendor.data import redis
    return redis
