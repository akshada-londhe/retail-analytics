from flask import Blueprint, render_template, request, session, redirect

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("Request Method:", request.method)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print("Username:", username)
        print("Password:", password)

        if username == 'admin' and password == 'admin':
            session['user'] = username
            print("Session after login:", dict(session))
            return redirect('/')

        print("Invalid Login")
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')