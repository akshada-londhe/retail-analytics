from flask import Flask
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.route("/")
    def home():
        return {
            "message": "Retail Analytics API",
            "status": "Running"
        }, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)