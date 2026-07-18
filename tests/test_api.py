import pytest
from app import create_app
from config import TestingConfig


@pytest.fixture
def client():
    """Create test client."""
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client


def test_api_dashboard(client):
    """Test dashboard API."""
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_sales' in data


def test_api_monthly_sales(client):
    """Test monthly sales API."""
    response = client.get('/api/sales/monthly')
    assert response.status_code == 200


def test_api_top_products(client):
    """Test top products API."""
    response = client.get('/api/top-products?n=5')
    assert response.status_code == 200
    data = response.get_json()
    assert 'top_products' in data


def test_api_sales_by_region(client):
    """Test sales by region API."""
    response = client.get('/api/sales/by-region')
    assert response.status_code == 200
    data = response.get_json()
    assert 'sales_by_region' in data


def test_landing_page(client):
    """Test landing page renders at /."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Smart Retail Analytics' in response.data


def test_signup_page_get(client):
    """Test signup page renders at /signup."""
    response = client.get('/signup')
    assert response.status_code == 200
    assert b'Create Account' in response.data


def test_signup_post_creates_user(client):
    """Test signup POST creates a user and logs in."""
    response = client.post('/signup', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123',
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'] == '/dashboard'

    with client.session_transaction() as sess:
        assert sess.get('user') == 'newuser'


def test_signup_duplicate_username(client):
    """Test signup rejects duplicate username."""
    client.post('/signup', data={
        'username': 'dupuser',
        'email': 'dup1@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123',
    })
    response = client.post('/signup', data={
        'username': 'dupuser',
        'email': 'dup2@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123',
    })
    assert response.status_code == 200
    assert b'already taken' in response.data


def test_dashboard_requires_login(client):
    """Test dashboard redirects to login when not authenticated."""
    response = client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
