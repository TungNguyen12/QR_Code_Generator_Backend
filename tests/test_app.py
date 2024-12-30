import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_generate_qr_success(client):
    response = client.post('/generate', json={'url': 'https://example.com'})  # Sending as JSON
    assert response.status_code == 200
    assert response.content_type == 'image/png'

def test_generate_qr_failure(client):
    response = client.post('/generate', json={'url': ''})  # Sending as JSON
    assert response.status_code == 400
    assert b"No URL provided" in response.data
