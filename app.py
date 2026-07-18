from flask import Flask
from config import DevelopmentConfig
from models import db, User
import os


def create_app(config_class=DevelopmentConfig):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from routes.landing import landing
    app.register_blueprint(landing)

    from routes.dashboard import dashboard
    app.register_blueprint(dashboard)

    from routes.api import api
    app.register_blueprint(api)

    from routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from routes.auth import auth
    app.register_blueprint(auth)

    from routes.reports import reports_bp
    app.register_blueprint(reports_bp)

    # Create directories at runtime, not import time
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()

        # Create default admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

    print("\n===== Registered Routes =====")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("=============================\n")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
