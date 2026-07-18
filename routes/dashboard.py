from flask import Blueprint, render_template, session, redirect
from models import Upload

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
def view_dashboard():
    if not session.get('user'):
        return redirect('/login')

    uploads = Upload.query.order_by(Upload.uploaded_at.desc()).all()
    has_uploads = len(uploads) > 0
    return render_template('dashboard.html', uploads=uploads, has_uploads=has_uploads)
