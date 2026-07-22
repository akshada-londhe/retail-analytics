
import pytest
import pandas as pd
from services.analytics import (
    total_sales, total_profit, average_order_value,
    top_products, top_customers, get_dashboard_kpis
)


@pytest.fixture
def sample_df():
    """Create sample DataFrame."""
    return pd.DataFrame({
        'Product': ['A', 'B', 'A', 'C', 'B'],
        'Customer': ['X', 'Y', 'X', 'Z', 'Y'],
        'Region': ['East', 'West', 'East', 'South', 'West'],
        'Category': ['Tech', 'Office', 'Tech', 'Furniture', 'Office'],
        'Sales': [500, 100, 300, 200, 150],
        'Profit': [100, 20, 60, 40, 30],
        'Profit Margin %': [20, 20, 20, 20, 20],
        'Month': [1, 1, 1, 2, 2]
    })


def test_total_sales(sample_df):
    """Test total sales calculation."""
    assert total_sales(sample_df) == 1250


def test_total_profit(sample_df):
    """Test total profit calculation."""
    assert total_profit(sample_df) == 250


def test_average_order_value(sample_df):
    """Test average order value."""
    assert average_order_value(sample_df) == 250


def test_top_products(sample_df):
    """Test top products."""
    result = top_products(sample_df, n=2)
    assert len(result) == 2
    assert result.index[0] == 'A'


def test_top_customers(sample_df):
    """Test top customers."""
    result = top_customers(sample_df, n=2)
    assert len(result) == 2
    assert result.index[0] == 'X'


def test_get_dashboard_kpis(sample_df):
    """Test dashboard KPIs."""
    kpis = get_dashboard_kpis(sample_df)
    assert kpis['total_sales'] == 1250
    assert kpis['total_profit'] == 250
    assert kpis['unique_customers'] == 3
    assert kpis['total_orders'] == 5
