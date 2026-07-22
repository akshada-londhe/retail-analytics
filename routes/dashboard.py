"""Page routing for dashboard, customers, and products."""

from flask import Blueprint, render_template, session
from models import User
from utils.auth import login_required

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard/')
@login_required
def view_dashboard():
    """Render dashboard page."""
    user = User.query.filter_by(username=session.get('user')).first()
    has_uploads = len(user.uploads) > 0 if user else False
    return render_template('dashboard.html', has_uploads=has_uploads)


@dashboard.route('/customers/')
@login_required
def view_customers():
    """Render customers page."""
    user = User.query.filter_by(username=session.get('user')).first()
    has_uploads = len(user.uploads) > 0 if user else False
    return render_template('customers.html', has_uploads=has_uploads)


@dashboard.route('/products/')
@login_required
def view_products():
    """Render products page."""
    user = User.query.filter_by(username=session.get('user')).first()
    has_uploads = len(user.uploads) > 0 if user else False
    return render_template('products.html', has_uploads=has_uploads)
