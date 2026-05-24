import os
import tempfile
import pytest
from datetime import datetime
from flaskr import create_app
from flaskr.database import database, init_database
from flaskr.models import User, Post


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    })

    with app.app_context():
        init_database()
        test_user = User(
            username='test',
            password='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'
        )
        other_user = User(
            username='other',
            password='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'
        )
        
        database.session.add(test_user)
        database.session.add(other_user)
        database.session.commit()

        post = Post(
            title='test title',
            body='test body',
            author_id = test_user.id,
            created=datetime.fromisoformat('2018-01-01 00:00:00')
        )

        database.session.add(post)
        database.session.commit()
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
