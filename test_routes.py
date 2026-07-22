import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app()

print('=== ROUTE LIST ===')
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        methods = ','.join(sorted(rule.methods))
        print(f'{rule.rule:40} -> {rule.endpoint:20} ({methods})')

print()
print('=== TESTING ALL ROUTES ===')
with app.test_client() as client:
    # Test without login - should redirect
    for route in ['/dashboard/', '/customers/', '/products/', '/reports/', '/upload/']:
        resp = client.get(route)
        print(f'{route:15} -> Status: {resp.status_code} (redirect to: {resp.headers.get("Location", "None")})')

    # Login
    with client.session_transaction() as sess:
        sess['user'] = 'admin'
    
    print()
    print('=== TESTING WITH LOGGED IN USER ===')
    for route in ['/dashboard/', '/customers/', '/products/', '/reports/', '/upload/']:
        resp = client.get(route)
        print(f'{route:15} -> Status: {resp.status_code}')