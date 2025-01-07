import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_app_initialized():
    """Test if the Flask app is initialized."""
    assert app is not None
    assert app.debug is False  # Assuming DEBUG=False in your config


def test_blueprints_registered():
    """Test if blueprints are registered with correct prefixes."""
    assert any(rule.startswith('/auth') for rule in [rule.rule for rule in app.url_map.iter_rules()])
    assert any(rule.startswith('/qrcodes') for rule in [rule.rule for rule in app.url_map.iter_rules()])
    assert any(rule.startswith('/') for rule in [rule.rule for rule in app.url_map.iter_rules()])


def test_index_route(client):
    """Test if the index page is reachable."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>QR Code Generator</title>' in response.data