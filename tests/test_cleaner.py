import pytest
import pandas as pd
from utils.cleaner import remove_duplicates, fix_dates, remove_negative_sales, clean_data


@pytest.fixture
def sample_df():
    """Create sample DataFrame."""
    return pd.DataFrame({
        'Order Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Ship Date': ['2023-01-05', '2023-01-06', '2023-01-07'],
        'Customer': ['Alice ', ' Bob', 'Charlie'],
        'Region': ['East', 'West', 'South'],
        'State': ['NY', 'CA', 'TX'],
        'Category': ['Tech', 'Office', 'Furniture'],
        'Sales': [500, 100, 200],
        'Profit': [100, 20, 40]
    })


def test_remove_duplicates():
    """Test duplicate removal."""
    df = pd.DataFrame({
        'Order Date': ['2023-01-01', '2023-01-01'],
        'Customer': ['Alice', 'Alice'],
        'Sales': [500, 500]
    })
    result = remove_duplicates(df)
    assert len(result) == 1


def test_fix_dates(sample_df):
    """Test date conversion."""
    result = fix_dates(sample_df)
    assert pd.api.types.is_datetime64_any_dtype(result['Order Date'])


def test_remove_negative_sales():
    """Test negative sales removal."""
    df = pd.DataFrame({'Sales': [100, -50, 200, 0]})
    result = remove_negative_sales(df)
    assert len(result) == 2
    assert all(result['Sales'] > 0)


def test_clean_data(sample_df):
    """Test master clean function."""
    result = clean_data(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
