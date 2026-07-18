"""API endpoints for retail analytics data."""

from flask import Blueprint, jsonify, request, session
from services.analytics import (
    get_dashboard_kpis,
    get_customer_metrics,
    get_product_metrics,
    calculate_rfm_segments
)
from utils.load_data import load_dataset
from utils.cleaner import clean_data
from services.features import engineer_features
from models import User, Upload
from utils.auth import api_login_required

api = Blueprint('api', __name__, url_prefix='/api')

# Global DataFrame Cache to prevent reloading and reprocessing
_DF_CACHE = {}


def get_user_latest_upload():
    """Get active or latest upload of the logged-in user."""
    username = session.get('user')
    if not username:
        return None
    user = User.query.filter_by(username=username).first()
    if not user or not user.uploads:
        return None
        
    active_upload_id = session.get('active_upload_id')
    if active_upload_id:
        upload = Upload.query.filter_by(id=active_upload_id, user_id=user.id).first()
        if upload:
            return upload
            
    return Upload.query.filter_by(user_id=user.id).order_by(Upload.uploaded_at.desc()).first()


def get_processed_df(upload_id=None):
    """Get cached processed DataFrame for active upload."""
    if upload_id:
        upload = Upload.query.get(upload_id)
    else:
        upload = get_user_latest_upload()

    if not upload:
        return None

    filepath = upload.filepath
    if filepath not in _DF_CACHE:
        _DF_CACHE[filepath] = engineer_features(clean_data(load_dataset(filepath)))
    return _DF_CACHE[filepath]


@api.route('/uploads', methods=['GET'])
@api_login_required
def api_list_uploads():
    """List all uploaded files for the logged in user."""
    try:
        username = session.get('user')
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        uploads = Upload.query.filter_by(user_id=user.id).order_by(Upload.uploaded_at.desc()).all()
        return jsonify({
            'uploads': [
                {
                    'id': u.id,
                    'filename': u.filename,
                    'rows_count': u.rows_count,
                    'uploaded_at': u.uploaded_at.isoformat() if u.uploaded_at else None,
                    'user': u.user.username if u.user else None
                }
                for u in uploads
            ]
        }), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/dashboard', methods=['GET'])
@api_login_required
def api_dashboard():
    """Get dashboard KPIs."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        kpis = get_dashboard_kpis(df)
        return jsonify(kpis), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/monthly', methods=['GET'])
@api_login_required
def api_monthly_sales():
    """Get monthly sales."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        monthly = df.groupby('Month')['Sales'].sum().to_dict()
        return jsonify({'monthly_sales': monthly}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/top-products', methods=['GET'])
@api_login_required
def api_top_products():
    """Get top products."""
    try:
        n = request.args.get('n', 5, type=int)
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        top = df.groupby('Product')['Sales'].sum().nlargest(n).to_dict()
        return jsonify({'top_products': top}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/by-region', methods=['GET'])
@api_login_required
def api_sales_by_region():
    """Get sales by region."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        region_sales = df.groupby('Region')['Sales'].sum().to_dict()
        return jsonify({'sales_by_region': region_sales}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/by-category', methods=['GET'])
@api_login_required
def api_sales_by_category():
    """Get sales by category."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        category_sales = df.groupby('Category')['Sales'].sum().to_dict()
        return jsonify({'sales_by_category': category_sales}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/customers', methods=['GET'])
@api_login_required
def api_customers():
    """Get list of customers with sales metrics."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        customers = get_customer_metrics(df)
        return jsonify({'customers': customers}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/customers/rfm', methods=['GET'])
@api_login_required
def api_customers_rfm():
    """Get RFM customer segments count."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        rfm_counts = calculate_rfm_segments(df)
        return jsonify({'rfm_segments': rfm_counts}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/products', methods=['GET'])
@api_login_required
def api_products():
    """Get list of products with performance metrics."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400
            
        products = get_product_metrics(df)
        return jsonify({'products': products}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500
