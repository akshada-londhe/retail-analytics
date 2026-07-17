from flask import Blueprint, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from config import Config
from models import db, Upload
from utils.validators import validate_upload, get_safe_filename
from utils.load_data import load_dataset


upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload."""
    if request.method == 'GET':
        return render_template('upload.html')
    
    if 'file' not in request.files:
        return render_template('upload.html', error='No file selected'), 400
    
    file = request.files['file']
    
    is_valid, error_msg = validate_upload(file)
    if not is_valid:
        return render_template('upload.html', error=error_msg), 400
    
    try:
        filename = get_safe_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Load and count rows
        df = load_dataset(filepath)
        rows_count = len(df)
        
        # Save to database
        upload = Upload(filename=filename, filepath=filepath, rows_count=rows_count, user_id=1)
        db.session.add(upload)
        db.session.commit()
        
        return render_template('upload.html', success=f'Uploaded {rows_count} rows'), 200
    except Exception as e:
        return render_template('upload.html', error=str(e)), 500