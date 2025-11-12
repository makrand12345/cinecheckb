import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the API' in response.data

def test_users_endpoint(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 200

def test_items_endpoint(client):
    response = client.get('/api/v1/items')
    assert response.status_code == 200