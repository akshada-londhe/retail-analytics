from flask import Blueprint, render_template, request, session, redirect

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        if username == 'admin' and password == 'admin':
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@auth.route('/logout')
def logout():
    """Handle logout."""
    session.pop('user', None)
    return redirect('/dashboard')