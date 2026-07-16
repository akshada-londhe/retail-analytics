import pytest
import pandas as pd
from services.features import (
    add_profit_margin, add_time_features, 
    add_customer_metrics, engineer_features
)


@pytest.fixture
def sample_df():
    """Create sample DataFrame."""
    return pd.DataFrame({
        'Order Date': ['2023-01-01', '2023-01-15', '2023-02-01'],
        'Customer': ['Alice', 'Bob', 'Alice'],
        'Sales': [500, 100, 300],
        'Profit': [100, 20, 60],
        'Discount': [0.0, 0.2, 0.1]
    })


def test_add_profit_margin(sample_df):
    """Test profit margin calculation."""
    result = add_profit_margin(sample_df)
    expected = 100 / 500 * 100
    assert result['Profit Margin %'].iloc[0] == expected


def test_add_time_features(sample_df):
    """Test time feature extraction."""
    result = add_time_features(sample_df)
    assert 'Year' in result.columns
    assert 'Month' in result.columns
    assert result['Month'].iloc[0] == 1
    assert result['Month'].iloc[2] == 2


def test_add_customer_metrics(sample_df):
    """Test customer metrics."""
    result = add_customer_metrics(sample_df)
    assert 'Customer_Total_Sales' in result.columns
    alice_total = result[result['Customer'] == 'Alice']['Customer_Total_Sales'].iloc[0]
    assert alice_total == 800


def test_engineer_features(sample_df):
    """Test full feature engineering."""
    result = engineer_features(sample_df)
    expected_cols = ['Year', 'Month', 'Quarter', 'Profit Margin %', 
                    'Discount Amount', 'Customer_Total_Sales']
    for col in expected_cols:
        assert col in result.columns