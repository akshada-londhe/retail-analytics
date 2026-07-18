from flask import Blueprint, render_template, session

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def view_dashboard():
    print("Dashboard Session:", dict(session))
    return render_template('dashboard.html')