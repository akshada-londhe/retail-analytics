from flask import Flask
from config import DevelopmentConfig
from models import db


def create_app(config_class=DevelopmentConfig):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from routes.dashboard import dashboard
    app.register_blueprint(dashboard)

    from routes.api import api
    app.register_blueprint(api)

    from routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from routes.auth import auth
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    print("\n===== Registered Routes =====")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("=============================\n")


    return app   



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)