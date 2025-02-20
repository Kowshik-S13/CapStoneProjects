import pytest

from app import create_app

@pytest.fixture()
def app():
    app = create_app()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    response = client.post('/', json={'username': 'kowshik', 'password': 'kowshik'})
    return response.get_json()['token']