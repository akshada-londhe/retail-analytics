import pytest
from app import create_app
from config import TestingConfig


@pytest.fixture
def client():
    """Create test client."""
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_client(client):
    """Create an authenticated test client."""
    with client.session_transaction() as sess:
        sess['user'] = 'admin'
    return client


@pytest.fixture
def auth_client_with_upload(client):
    """Create an authenticated test client with an uploaded dataset."""
    from models import User, Upload, db
    with client.session_transaction() as sess:
        sess['user'] = 'admin'

    with client.application.app_context():
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # Clean old uploads
            Upload.query.filter_by(user_id=admin.id).delete()
            
            # Create a sample upload referencing data/superstore.csv
            upload = Upload(
                filename='superstore.csv',
                filepath='data/superstore.csv',
                rows_count=9994,
                user_id=admin.id
            )
            db.session.add(upload)
            db.session.commit()
            
    return client


def test_api_dashboard(auth_client_with_upload):
    """Test dashboard API."""
    response = auth_client_with_upload.get('/api/dashboard')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_sales' in data


def test_api_monthly_sales(auth_client_with_upload):
    """Test monthly sales API."""
    response = auth_client_with_upload.get('/api/sales/monthly')
    assert response.status_code == 200


def test_api_top_products(auth_client_with_upload):
    """Test top products API."""
    response = auth_client_with_upload.get('/api/top-products?n=5')
    assert response.status_code == 200
    data = response.get_json()
    assert 'top_products' in data


def test_api_sales_by_region(auth_client_with_upload):
    """Test sales by region API."""
    response = auth_client_with_upload.get('/api/sales/by-region')
    assert response.status_code == 200
    data = response.get_json()
    assert 'sales_by_region' in data


def test_api_customers(auth_client_with_upload):
    """Test customers API."""
    response = auth_client_with_upload.get('/api/customers')
    assert response.status_code == 200
    data = response.get_json()
    assert 'customers' in data


def test_api_customers_rfm(auth_client_with_upload):
    """Test customers RFM API."""
    response = auth_client_with_upload.get('/api/customers/rfm')
    assert response.status_code == 200
    data = response.get_json()
    assert 'rfm_segments' in data


def test_api_products(auth_client_with_upload):
    """Test products API."""
    response = auth_client_with_upload.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert 'products' in data


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
    assert response.headers['Location'] == '/dashboard/'

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
