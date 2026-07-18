from flask import Blueprint, jsonify, request, g
from services.analytics import get_dashboard_kpis
from utils.load_data import load_dataset
from utils.cleaner import clean_data
from services.features import engineer_features
from models import Upload

api = Blueprint('api', __name__, url_prefix='/api')


def get_processed_df(filepath=None):
    """Get cached processed DataFrame."""
    if filepath is None:
        filepath = 'data/superstore.csv'

    cache_key = f'df_{filepath}'
    if cache_key not in g:
        g.__dict__[cache_key] = engineer_features(clean_data(load_dataset(filepath)))
    return g.__dict__[cache_key]


@api.route('/uploads', methods=['GET'])
def api_list_uploads():
    """List all uploaded files."""
    try:
        uploads = Upload.query.order_by(Upload.uploaded_at.desc()).all()
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
def api_dashboard():
    """Get dashboard KPIs."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        if upload_id:
            upload = Upload.query.get(upload_id)
            if not upload:
                return jsonify({'error': 'Upload not found'}), 404
            df = get_processed_df(upload.filepath)
        else:
            df = get_processed_df()
        kpis = get_dashboard_kpis(df)
        return jsonify(kpis), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/monthly', methods=['GET'])
def api_monthly_sales():
    """Get monthly sales."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        if upload_id:
            upload = Upload.query.get(upload_id)
            if not upload:
                return jsonify({'error': 'Upload not found'}), 404
            df = get_processed_df(upload.filepath)
        else:
            df = get_processed_df()
        monthly = df.groupby('Month')['Sales'].sum().to_dict()
        return jsonify({'monthly_sales': monthly}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/top-products', methods=['GET'])
def api_top_products():
    """Get top products."""
    try:
        n = request.args.get('n', 5, type=int)
        upload_id = request.args.get('upload_id', type=int)
        if upload_id:
            upload = Upload.query.get(upload_id)
            if not upload:
                return jsonify({'error': 'Upload not found'}), 404
            df = get_processed_df(upload.filepath)
        else:
            df = get_processed_df()
        top = df.groupby('Product')['Sales'].sum().nlargest(n).to_dict()
        return jsonify({'top_products': top}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/by-region', methods=['GET'])
def api_sales_by_region():
    """Get sales by region."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        if upload_id:
            upload = Upload.query.get(upload_id)
            if not upload:
                return jsonify({'error': 'Upload not found'}), 404
            df = get_processed_df(upload.filepath)
        else:
            df = get_processed_df()
        region_sales = df.groupby('Region')['Sales'].sum().to_dict()
        return jsonify({'sales_by_region': region_sales}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500


@api.route('/sales/by-category', methods=['GET'])
def api_sales_by_category():
    """Get sales by category."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        if upload_id:
            upload = Upload.query.get(upload_id)
            if not upload:
                return jsonify({'error': 'Upload not found'}), 404
            df = get_processed_df(upload.filepath)
        else:
            df = get_processed_df()
        category_sales = df.groupby('Category')['Sales'].sum().to_dict()
        return jsonify({'sales_by_category': category_sales}), 200
    except (ValueError, FileNotFoundError, KeyError) as e:
        return jsonify({'error': str(e)}), 500
