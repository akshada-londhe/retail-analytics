from flask import Blueprint, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# In-memory user store (dictionary)
# Format: {username: {'email': email, 'password_hash': hash}}
users_store = {}


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        error = None
        if not username or not email or not password:
            error = 'All fields are required.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif username in users_store:
            error = 'Username already taken.'
        elif any(u['email'] == email for u in users_store.values()):
            error = 'Email already registered.'

        if error:
            return render_template('signup.html', error=error)

        # Store user with hashed password
        users_store[username] = {
            'email': email,
            'password_hash': generate_password_hash(password)
        }

        session['user'] = username
        return redirect('/dashboard/')
    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_store.get(username)

        if user and check_password_hash(user['password_hash'], password):
            session['user'] = username
            return redirect('/dashboard/')

        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')