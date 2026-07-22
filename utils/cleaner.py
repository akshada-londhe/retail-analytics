import pandas as pd


def remove_duplicates(df):
    """Remove duplicate rows from DataFrame."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Removed {before - after} duplicate rows")
    return df


def fix_dates(df):
    """Convert date columns to datetime dtype."""
    date_columns = ['Order Date', 'Ship Date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='mixed', errors='coerce')
    return df


def remove_nulls(df):
    """Remove rows with null values."""
    before = len(df)
    df = df.dropna()
    after = len(df)
    print(f"Removed {before - after} rows with nulls")
    return df


def remove_negative_sales(df):
    """Remove rows with negative or zero sales."""
    before = len(df)
    df = df[df['Sales'] > 0]
    after = len(df)
    print(f"Removed {before - after} rows with non-positive sales")
    return df


def standardize_text(df):
    """Standardize text columns (strip whitespace)."""
    text_columns = ['Customer', 'Region', 'State', 'Category', 'Sub Category']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip()
    return df


def clean_data(df, remove_nulls_flag=True, remove_negative_flag=True):
    """Master data cleaning function."""
    print("Starting data cleaning...")

    # Standardize column headers for alternative Superstore formats
    rename_dict = {
        'Customer Name': 'Customer',
        'Product Name': 'Product',
        'Sub-Category': 'Sub Category'
    }
    df = df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns})

    df = remove_duplicates(df)
    df = fix_dates(df)
    df = standardize_text(df)

    if remove_nulls_flag:
        df = remove_nulls(df)

    if remove_negative_flag:
        df = remove_negative_sales(df)

    print(f"Cleaning complete. Final shape: {df.shape}")
    return df
