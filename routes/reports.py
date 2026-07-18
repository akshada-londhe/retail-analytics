from flask import Blueprint, jsonify, send_file, g, current_app
from services.reports import generate_csv_report, generate_excel_report, generate_summary_report
from services.analytics import get_dashboard_kpis
from utils.load_data import load_dataset
from utils.cleaner import clean_data
from services.features import engineer_features
import os

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


def get_processed_df():
    """Get cached processed DataFrame."""
    if 'report_df' not in g:
        g.report_df = engineer_features(clean_data(load_dataset('data/superstore.csv')))
    return g.report_df


@reports_bp.route('/summary', methods=['GET'])
def summary_report():
    """Generate and download summary report."""
    try:
        df = get_processed_df()
        kpis = get_dashboard_kpis(df)
        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'summary_report.txt')
        generate_summary_report(df, kpis, output_path)
        return send_file(output_path, as_attachment=True, download_name='summary_report.txt')
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/csv', methods=['GET'])
def csv_report():
    """Generate and download CSV report."""
    try:
        df = get_processed_df()
        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'data_export.csv')
        generate_csv_report(df, output_path)
        return send_file(output_path, as_attachment=True, download_name='data_export.csv')
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/excel', methods=['GET'])
def excel_report():
    """Generate and download Excel report."""
    try:
        df = get_processed_df()
        output_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'data_export.xlsx')
        generate_excel_report(df, output_path)
        return send_file(output_path, as_attachment=True, download_name='data_export.xlsx')
    except (ValueError, FileNotFoundError, KeyError, OSError) as e:
        return jsonify({'error': str(e)}), 500
