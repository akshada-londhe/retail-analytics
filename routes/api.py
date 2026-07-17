from flask import Blueprint, jsonify, request
from services.analytics import get_dashboard_kpis
from utils.load_data import load_dataset
from utils.cleaner import clean_data
from services.features import engineer_features

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/dashboard', methods=['GET'])
def api_dashboard():
    """Get dashboard KPIs."""
    try:
        df = load_dataset('data/superstore.csv')
        df = clean_data(df)
        df = engineer_features(df)
        kpis = get_dashboard_kpis(df)
        return jsonify(kpis), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/monthly', methods=['GET'])
def api_monthly_sales():
    """Get monthly sales."""
    try:
        df = load_dataset('data/superstore.csv')
        df = clean_data(df)
        df = engineer_features(df)
        monthly = df.groupby('Month')['Sales'].sum().to_dict()
        return jsonify({'monthly_sales': monthly}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/top-products', methods=['GET'])
def api_top_products():
    """Get top products."""
    try:
        n = request.args.get('n', 5, type=int)
        df = load_dataset('data/superstore.csv')
        df = clean_data(df)
        df = engineer_features(df)
        
        top = df.groupby('Product')['Sales'].sum().nlargest(n).to_dict()
        return jsonify({'top_products': top}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/by-region', methods=['GET'])
def api_sales_by_region():
    """Get sales by region."""
    try:
        df = load_dataset('data/superstore.csv')
        df = clean_data(df)
        df = engineer_features(df)
        
        region_sales = df.groupby('Region')['Sales'].sum().to_dict()
        return jsonify({'sales_by_region': region_sales}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500