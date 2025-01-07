import pytest
import json
from src.app.auth.utils import decode_token
from src.config import JWT_SECRET_KEY
import jwt
from datetime import datetime, timedelta

from app import app
from src.db.database import get_db


# Fixture to set up the test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Fixture to clear the database before each test
@pytest.fixture(autouse=True)
def clear_database():
    db = get_db()
    db.users.delete_many({})


# Test the registration route
def test_register_user(client):
    # Test successful registration
    data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    response = client.post('/auth/register', json=data)
    assert response.status_code == 201
    assert 'user_id' in response.json
    assert "User registered successfully" in response.json['message']

    # Test registration with missing fields
    data = {"username": "testuser", "email": "test@example.com"}
    response = client.post('/auth/register', json=data)
    assert response.status_code == 400
    assert "All fields are required" in response.json['error']

    # Test duplicate user registration
    response = client.post('/auth/register', json={"username": "testuser", "email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 400
    assert "User already exists" in response.json['error']


# Test the login route
def test_login_user(client):
    # Register a test user first
    client.post('/auth/register', json={"username": "testuser", "email": "test@example.com", "password": "testpassword"})


    # Test successful login
    data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json
    assert "Login successful" in response.json['message']

    # Test login with missing fields
    data = {"email": "test@example.com"}
    response = client.post('/auth/login', json=data)
    assert response.status_code == 400
    assert "Email and password are required" in response.json['error']


    # Test login with incorrect password
    data = {"email": "test@example.com", "password": "wrongpassword"}
    response = client.post('/auth/login', json=data)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json['error']


    # Test login with invalid email
    data = {"email": "invalid@example.com", "password": "testpassword"}
    response = client.post('/auth/login', json=data)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json['error']


# Test refresh token route
def test_refresh_token(client):
   # Register and login a test user first
    client.post('/auth/register', json={"username": "testuser", "email": "test@example.com", "password": "testpassword"})
    login_response = client.post('/auth/login', json={"email": "test@example.com", "password": "testpassword"})
    refresh_token = login_response.json['refresh_token']

    # Test successful refresh
    response = client.post('/auth/auth/refresh', json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json
   
    # Test refresh with invalid refresh token
    response = client.post('/auth/auth/refresh', json={"refresh_token": "invalid_token"})
    assert response.status_code == 401
    assert "Invalid or expired refresh token" in response.json['error']