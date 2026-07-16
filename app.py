from flask import Flask
from config import DevelopmentConfig
from models import db


def create_app(config_class=DevelopmentConfig):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def home():
        return {'message': 'Retail Analytics API'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)