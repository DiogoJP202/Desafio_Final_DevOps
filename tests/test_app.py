import pytest
import werkzeug
from flask_jwt_extended import create_access_token
from app import app

# Patch para manter compatibilidade com werkzeug em ambientes onde __version__ pode faltar
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.app_context():
        yield app.test_client()


@pytest.fixture()
def auth_header():
    # Cria um token JWT valido para testes protegidos
    with app.app_context():
        token = create_access_token(identity="user")
    return {"Authorization": f"Bearer {token}"}


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API is running"}


def test_login_returns_access_token(client):
    response = client.get('/login')
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data and data['access_token']


def test_protected_requires_token(client):
    response = client.post('/protected')
    assert response.status_code == 401

