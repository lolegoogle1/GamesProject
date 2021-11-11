import pytest
import sys

sys.path.append('..')

from app import app, Base, engine, session as db_session
from app.models import User, Company


@pytest.fixture(scope='function')
def testapp():
    _app = app

    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.fixture(scope='function')
def session(testapp):
    ctx = testapp.app_context()
    ctx.push()

    yield db_session

    db_session.close_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user(session):
    user = User(
        name='TestUser',
        login='TestUserTestLogin',
        password='TestPassword',
    )
    session.add(user)
    session.commit()

    return user


@pytest.fixture()
def client(testapp):
    return testapp.test_client()


@pytest.fixture()
def user_token(user, client):
    res = client.post('/users/login', json={
        'login': user.login,
        'password': 'TestPassword'
    })
    return res.get_json()['access_token']


@pytest.fixture()
def user_headers(user_token):
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    return headers


@pytest.fixture()
def companies(session):
    company = Company(
        name='TestCompany',
        description='TestDescription',
        founded_date='2000-01-01'
    )
    session.add(company)
    session.commit()

    return company

# TODO
# game fixture
# test_game_model
