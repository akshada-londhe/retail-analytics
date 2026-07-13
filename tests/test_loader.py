"""Tests for data loader."""

import pytest
import pandas as pd
from pathlib import Path
from utils.load_data import load_dataset, inspect_dataset


@pytest.fixture
def sample_csv(tmp_path):
    """Create temp CSV for testing."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("A,B\n1,2\n3,4")
    return str(csv_file)


def test_load_dataset_success(sample_csv):
    """Test loading valid CSV."""
    df = load_dataset(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['A', 'B']


def test_load_dataset_file_not_found():
    """Test error when file missing."""
    with pytest.raises(FileNotFoundError):
        load_dataset('nonexistent.csv')


def test_load_dataset_not_csv(tmp_path):
    """Test error when not CSV."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("test")
    
    with pytest.raises(ValueError, match="Expected .csv"):
        load_dataset(str(txt_file))


def test_inspect_dataset(sample_csv, capsys):
    """Test dataset inspection."""
    df = load_dataset(sample_csv)
    inspect_dataset(df)
    captured = capsys.readouterr()
    
    assert "Shape:" in captured.out
    assert "Columns:" in captured.out