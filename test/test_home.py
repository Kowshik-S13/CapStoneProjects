import base64
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.drop_all()

def test_home(client):
    # Assuming you have a way to authenticate and get a token
    # For example, you might have a login endpoint to get a token
    response = client.post('/', json={'username': 'kowshik', 'password': 'kowshik'})
    print(response.data)
    token = response.json['token']

    # Use the token to access the /home endpoint
    response = client.get('/', headers={'Authorization': f'Bearer {token}'})
    assert b'Welcome to the User API' in response.data


# # from ..app.models import User
# def test_unauthorized_access(client):
#     response = client.get('/')
#     assert response.status_code == 401
#     assert b'WWW-Authenticate' in response.headers.keys()

# def test_home(client):
#     credentials = base64.b64encode(b"testuser:testpassword").decode("utf-8")
#     response = client.get("/")
#     assert b"Welcome to the User API" in response.data


# def test_registration(client, app):
#     response = client.post("/register", data={"email": "test@test.com", "password": "testpassword"})

#     with app.app_context():
#         assert User.query.count() == 1
#         assert User.query.first().email == "test@test.com"

# @responses.activate
# def test_age(client):
#     responses.add(
#         responses.GET,
#         "https://api.agify.io",
#         json={"age": 33, "count": 1049384, "name": "Anthony"},
#         status=200
#     )
#     client.post("/register", data={"email": "test@test.com", "password": "testpassword"})
#     client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

#     response = client.post("/age", data={"name": "Anthony"})

#     assert b"You are 33 years old" in response.data

# def test_invalid_login(client):
#     client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

#     response = client.get("/city")

#     assert response.status_code == 401