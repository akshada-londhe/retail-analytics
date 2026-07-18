from datetime import datetime


def generate_csv_report(df, output_path):
    """Generate CSV report from DataFrame."""
    df.to_csv(output_path, index=False)
    return output_path


def generate_excel_report(df, output_path):
    """Generate Excel report from DataFrame."""
    df.to_excel(output_path, index=False, sheet_name='Analytics')
    return output_path


def generate_summary_report(df, kpis, output_path):
    """Generate text summary report with KPIs and top products/regions."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("RETAIL ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("KEY PERFORMANCE INDICATORS\n")
        f.write("-" * 40 + "\n")
        for key, value in kpis.items():
            f.write(f"{key}: {value}\n")

        f.write("\n\nTOP PRODUCTS BY SALES\n")
        f.write("-" * 40 + "\n")

        top_products = df.groupby('Product')['Sales'].sum().nlargest(5)
        for product, sales in top_products.items():
            f.write(f"{product}: ${sales:.2f}\n")

        f.write("\n\nSALES BY REGION\n")
        f.write("-" * 40 + "\n")

        region_sales = df.groupby('Region')['Sales'].sum()
        for region, sales in region_sales.items():
            f.write(f"{region}: ${sales:.2f}\n")

    return output_path
