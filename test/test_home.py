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
    credentials = base64.b64encode(b"admin:admin").decode("utf-8")
    response = client.get("/",headers={"Authorization": f"Basic {credentials}"})
    assert response.status_code == 200
    assert b"Welcome to the User API" in response.data