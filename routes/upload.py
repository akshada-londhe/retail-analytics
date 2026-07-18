from flask import Blueprint, render_template, request, session, redirect, current_app
import os
from models import db, Upload, User
from utils.validators import validate_upload, get_safe_filename
from utils.load_data import load_dataset

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload."""
    if request.method == 'GET':
        return render_template('upload.html')

    # Check if user is logged in
    if 'user' not in session:
        return redirect('/login')

    if 'file' not in request.files:
        return render_template('upload.html', error='No file selected'), 400

    file = request.files['file']

    is_valid, error_msg = validate_upload(file)
    if not is_valid:
        return render_template('upload.html', error=error_msg), 400

    try:
        filename = get_safe_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load CSV and count rows
        df = load_dataset(filepath)
        rows_count = len(df)

        # Get logged-in user
        user = User.query.filter_by(username=session.get('user')).first()

        if not user:
            return render_template(
                'upload.html',
                error='User not found. Please log in again.'
            ), 401

        # Save upload to database
        upload = Upload(
            filename=filename,
            filepath=filepath,
            rows_count=rows_count,
            user_id=user.id
        )

        db.session.add(upload)
        db.session.commit()

        return render_template(
            'upload.html',
            success=f'File uploaded successfully! {rows_count} rows imported.'
        ), 200

    except (ValueError, FileNotFoundError, OSError) as e:
        db.session.rollback()
        return render_template('upload.html', error=str(e)), 500
