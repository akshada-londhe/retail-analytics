"""Data upload and management blueprint routes."""

from flask import Blueprint, render_template, request, session, redirect, current_app
import os
from models import db, Upload, User
from utils.validators import validate_upload, get_safe_filename
from utils.load_data import load_dataset

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and list user datasets."""
    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(username=session.get('user')).first()
    if not user:
        return redirect('/login')

    uploads = Upload.query.filter_by(user_id=user.id).order_by(Upload.uploaded_at.desc()).all()
    
    # Auto-resolve active upload ID
    active_upload_id = session.get('active_upload_id')
    if not active_upload_id and uploads:
        active_upload_id = uploads[0].id
        session['active_upload_id'] = active_upload_id

    if request.method == 'GET':
        return render_template('upload.html', uploads=uploads, active_upload_id=active_upload_id)

    if 'file' not in request.files:
        return render_template(
            'upload.html', 
            error='No file selected', 
            uploads=uploads, 
            active_upload_id=active_upload_id
        ), 400

    file = request.files['file']

    is_valid, error_msg = validate_upload(file)
    if not is_valid:
        return render_template(
            'upload.html', 
            error=error_msg, 
            uploads=uploads, 
            active_upload_id=active_upload_id
        ), 400

    try:
        filename = get_safe_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load CSV and count rows
        df = load_dataset(filepath)
        rows_count = len(df)

        # Save upload to database
        upload = Upload(
            filename=filename,
            filepath=filepath,
            rows_count=rows_count,
            user_id=user.id
        )

        db.session.add(upload)
        db.session.commit()

        # Automatically activate the newly uploaded dataset
        session['active_upload_id'] = upload.id

        # Re-fetch uploads list after addition
        uploads = Upload.query.filter_by(user_id=user.id).order_by(Upload.uploaded_at.desc()).all()
        active_upload_id = upload.id

        return render_template(
            'upload.html',
            success=f'File uploaded successfully! {rows_count} rows imported.',
            uploads=uploads,
            active_upload_id=active_upload_id
        ), 200

    except (ValueError, FileNotFoundError, OSError) as e:
        db.session.rollback()
        return render_template(
            'upload.html', 
            error=str(e), 
            uploads=uploads, 
            active_upload_id=active_upload_id
        ), 500


@upload_bp.route('/upload/activate/<int:upload_id>', methods=['POST'])
def activate_dataset(upload_id):
    """Set an uploaded dataset as the active workspace."""
    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(username=session.get('user')).first()
    if not user:
        return redirect('/login')

    upload = Upload.query.filter_by(id=upload_id, user_id=user.id).first()
    if upload:
        session['active_upload_id'] = upload.id

    return redirect('/upload/')


@upload_bp.route('/upload/delete/<int:upload_id>', methods=['POST'])
def delete_dataset(upload_id):
    """Delete an uploaded dataset and clean up raw files."""
    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(username=session.get('user')).first()
    if not user:
        return redirect('/login')

    upload = Upload.query.filter_by(id=upload_id, user_id=user.id).first()
    if upload:
        if session.get('active_upload_id') == upload.id:
            session.pop('active_upload_id', None)

        # Remove local file if it exists
        try:
            if os.path.exists(upload.filepath):
                os.remove(upload.filepath)
        except OSError:
            pass

        db.session.delete(upload)
        db.session.commit()

    return redirect('/upload/')
