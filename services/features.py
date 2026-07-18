import pandas as pd


def add_time_features(df):
    """Add month, year, quarter columns."""
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Quarter'] = df['Order Date'].dt.quarter
    return df


def add_profit_margin(df):
    """Add profit margin percentage."""
    df['Profit Margin %'] = (df['Profit'] / df['Sales'] * 100).round(2)
    return df


def add_discount_impact(df):
    """Add discount impact features."""
    df['Discount Amount'] = df['Sales'] * df['Discount']
    df['Revenue After Discount'] = df['Sales'] - df['Discount Amount']
    return df


def add_customer_metrics(df):
    """Add customer-level metrics."""
    customer_stats = df.groupby('Customer').agg({
        'Sales': ['sum', 'count', 'mean'],
        'Profit': 'sum'
    }).reset_index()

    customer_stats.columns = [
        'Customer', 'Customer_Total_Sales',
        'Customer_Order_Count', 'Customer_Avg_Order',
        'Customer_Total_Profit'
    ]

    df = df.merge(customer_stats, on='Customer', how='left')
    return df


def engineer_features(df):
    """Master feature engineering function."""
    print("Starting feature engineering...")

    df = add_time_features(df)
    df = add_profit_margin(df)
    df = add_discount_impact(df)
    df = add_customer_metrics(df)

    print(f"Feature engineering complete. Shape: {df.shape}")
    return df
