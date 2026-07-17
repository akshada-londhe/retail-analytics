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