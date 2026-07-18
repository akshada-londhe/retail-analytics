"""Analytics services for retail data processing."""

import pandas as pd


def total_sales(df):
    """Calculate total sales."""
    return df['Sales'].sum()


def total_profit(df):
    """Calculate total profit."""
    return df['Profit'].sum()


def average_order_value(df):
    """Calculate average order value."""
    return df['Sales'].mean()


def profit_margin_avg(df):
    """Calculate average profit margin."""
    return df['Profit Margin %'].mean()


def top_products(df, n=5):
    """Get top N products by sales."""
    return df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(n)


def top_customers(df, n=5):
    """Get top N customers by sales."""
    return df.groupby('Customer')['Sales'].sum().sort_values(ascending=False).head(n)


def sales_by_region(df):
    """Get sales by region."""
    return df.groupby('Region')['Sales'].sum().sort_values(ascending=False)


def sales_by_category(df):
    """Get sales by category."""
    return df.groupby('Category')['Sales'].sum().sort_values(ascending=False)


def monthly_sales(df):
    """Get monthly sales totals."""
    return df.groupby('Month')['Sales'].sum()


def monthly_profit(df):
    """Get monthly profit totals."""
    return df.groupby('Month')['Profit'].sum()


def get_dashboard_kpis(df):
    """Get all KPIs for dashboard."""
    return {
        'total_sales': float(total_sales(df)),
        'total_profit': float(total_profit(df)),
        'avg_order_value': float(average_order_value(df)),
        'avg_profit_margin': float(profit_margin_avg(df)),
        'unique_customers': int(df['Customer'].nunique()),
        'unique_products': int(df['Product'].nunique()),
        'total_orders': len(df)
    }


def get_customer_metrics(df):
    """Get customer list with sales, count, average value, profit."""
    customer_stats = df.groupby('Customer').agg({
        'Sales': ['sum', 'count', 'mean'],
        'Profit': 'sum'
    }).reset_index()

    customer_stats.columns = [
        'Customer', 'TotalSales', 'OrderCount', 'AvgOrderValue', 'TotalProfit'
    ]
    # Sort by total sales descending
    customer_stats = customer_stats.sort_values(by='TotalSales', ascending=False)
    return customer_stats.to_dict(orient='records')


def get_product_metrics(df):
    """Get product list with sales, category, subcategory, profit, discount."""
    product_stats = df.groupby(['Product', 'Category', 'Sub Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Discount': 'mean'
    }).reset_index()

    product_stats.columns = [
        'Product', 'Category', 'SubCategory', 'TotalSales', 'TotalProfit', 'AvgDiscount'
    ]
    product_stats = product_stats.sort_values(by='TotalSales', ascending=False)
    return product_stats.to_dict(orient='records')


def calculate_rfm_segments(df):
    """Calculate RFM segments for customer segmentation."""
    # Find max date in dataset
    max_date = pd.to_datetime(df['Order Date'], format='mixed', errors='coerce').max()

    rfm = df.groupby('Customer').agg({
        'Order Date': lambda x: (max_date - pd.to_datetime(x, format='mixed', errors='coerce').max()).days,
        'Sales': ['count', 'sum']
    }).reset_index()

    rfm.columns = ['Customer', 'Recency', 'Frequency', 'Monetary']

    # Handle quintile cuts safely
    try:
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    except Exception:
        rfm['R_Score'] = 3

    try:
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    except Exception:
        rfm['F_Score'] = 3

    try:
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    except Exception:
        rfm['M_Score'] = 3

    rfm['R_Score'] = rfm['R_Score'].astype(int)
    rfm['F_Score'] = rfm['F_Score'].astype(int)
    rfm['M_Score'] = rfm['M_Score'].astype(int)

    def assign_segment(row):
        r = row['R_Score']
        f = row['F_Score']

        if r >= 4 and f >= 4:
            return 'Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f <= 2:
            return 'New Customers'
        elif r <= 2 and f >= 3:
            return 'At Risk'
        elif r <= 2 and f <= 2:
            return 'Hibernating / Lost'
        else:
            return 'General Customers'

    rfm['Segment'] = rfm.apply(assign_segment, axis=1)
    counts = rfm['Segment'].value_counts().to_dict()
    return counts
