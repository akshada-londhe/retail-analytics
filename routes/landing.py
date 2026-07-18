from flask import Blueprint, render_template

landing = Blueprint('landing', __name__)


@landing.route('/')
def view_landing():
    return render_template('landing.html')
