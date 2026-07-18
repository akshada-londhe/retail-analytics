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
