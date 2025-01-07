import pytest
from src.app.auth.models import find_user_by_email
from db.database import get_db

db = get_db()

@pytest.fixture
def client():
    from main import app
    with app.test_client() as client:
        yield client

def test_register_and_login(client):
    # Test registration
    response = client.post('/auth/register', json={
        "username": "test_user",
        "email": "test@example.com",
        "password": "secure_password"
    })
    assert response.status_code == 201

    # Verify user was created
    user = find_user_by_email("test@example.com")
    assert user is not None

    # Test login
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "secure_password"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()
