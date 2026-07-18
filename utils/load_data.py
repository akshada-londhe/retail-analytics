"""Load data from CSV files into Pandas DataFrames."""

import pandas as pd
from pathlib import Path


def load_dataset(filepath):
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if filepath.suffix.lower() != ".csv":
        raise ValueError("Expected .csv")

    try:
        df = pd.read_csv(filepath)

        # Convert date columns if they exist
        date_columns = ["Order Date", "Ship Date"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])

        return df

    except Exception as e:
        raise ValueError(f"Error reading CSV: {e}")


def inspect_dataset(df):
    """
    Display basic information about the dataset.
    """

    print("=" * 50)
    print("DATASET INFORMATION")
    print("=" * 50)

    print(f"\nShape: {df.shape}")

    print(f"\nColumns:\n{df.columns.tolist()}")

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nStatistical Summary:")
    print(df.describe(include="all"))
