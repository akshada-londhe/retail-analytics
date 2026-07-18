"""Report generation and download routes."""

from flask import Blueprint, jsonify, send_file, render_template, request, current_app, session
from services.reports import generate_csv_report, generate_excel_report, generate_summary_report
from services.analytics import get_dashboard_kpis
from models import User, Upload
from routes.api import get_processed_df
from utils.auth import login_required
import os

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/')
@login_required
def view_reports():
    """Render the reports dashboard page."""
    user = User.query.filter_by(username=session.get('user')).first()
    has_uploads = len(user.uploads) > 0 if user else False
    return render_template('reports.html', has_uploads=has_uploads)


@reports_bp.route('/preview', methods=['GET'])
@login_required
def preview_report():
    """Generate and return text summary preview."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400

        kpis = get_dashboard_kpis(df)
        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'temp_preview.txt')
        generate_summary_report(df, kpis, output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'preview': content}), 200
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/summary', methods=['GET'])
@login_required
def summary_report():
    """Generate and download summary report."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400

        if upload_id:
            upload = Upload.query.get(upload_id)
            filename = f"summary_report_{upload.filename}.txt"
        else:
            # Get user's latest upload
            from routes.api import get_user_latest_upload
            upload = get_user_latest_upload()
            filename = f"summary_report_{upload.filename}.txt" if upload else "summary_report.txt"

        kpis = get_dashboard_kpis(df)
        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'summary_report.txt')
        generate_summary_report(df, kpis, output_path)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/csv', methods=['GET'])
@login_required
def csv_report():
    """Generate and download CSV report."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400

        if upload_id:
            upload = Upload.query.get(upload_id)
            filename = f"data_export_{upload.filename}"
        else:
            from routes.api import get_user_latest_upload
            upload = get_user_latest_upload()
            filename = f"data_export_{upload.filename}" if upload else "data_export.csv"

        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'data_export.csv')
        generate_csv_report(df, output_path)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/excel', methods=['GET'])
@login_required
def excel_report():
    """Generate and download Excel report."""
    try:
        upload_id = request.args.get('upload_id', type=int)
        df = get_processed_df(upload_id)
        if df is None:
            return jsonify({'error': 'No uploaded dataset found. Please upload a dataset.'}), 400

        if upload_id:
            upload = Upload.query.get(upload_id)
            filename = f"data_export_{os.path.splitext(upload.filename)[0]}.xlsx"
        else:
            from routes.api import get_user_latest_upload
            upload = get_user_latest_upload()
            filename = f"data_export_{os.path.splitext(upload.filename)[0]}.xlsx" if upload else "data_export.xlsx"

        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'data_export.xlsx')
        generate_excel_report(df, output_path)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500
