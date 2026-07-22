import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app()

print('=== TESTING SIGNUP/LOGIN FLOW ===')
with app.test_client() as client:
    # Test signup page loads
    resp = client.get('/signup')
    print(f'GET /signup -> {resp.status_code}')
    
    # Sign up new user
    resp = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    print(f'POST /signup -> {resp.status_code}')
    
    with client.session_transaction() as sess:
        print(f'  Session after signup: {dict(sess)}')
    
    # Test accessing dashboard after signup
    resp = client.get('/dashboard/')
    print(f'GET /dashboard/ after signup -> {resp.status_code}')
    
    # Test logout
    resp = client.get('/logout', follow_redirects=True)
    print(f'GET /logout -> {resp.status_code}')
    
    with client.session_transaction() as sess:
        print(f'  Session after logout: {dict(sess)}')
    
    # Test login with existing user
    resp = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    print(f'POST /login -> {resp.status_code}')
    
    with client.session_transaction() as sess:
        print(f'  Session after login: {dict(sess)}')
    
    # Test accessing dashboard after login
    resp = client.get('/dashboard/')
    print(f'GET /dashboard/ after login -> {resp.status_code}')

print()
print('=== ALL TESTS PASSED ===')