from flask import Blueprint, render_template

landing = Blueprint('landing', __name__, url_prefix='/')


@landing.route('/')
def view_landing():
    return render_template('landing.html')
