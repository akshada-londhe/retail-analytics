from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def utcnow():
    """Return current UTC time with timezone info."""
    return datetime.now(timezone.utc)


class User(db.Model):
    """User model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    uploads = db.relationship('Upload', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)


class Upload(db.Model):
    """File upload model."""
    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rows_count = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=utcnow)

    reports = db.relationship('Report', backref='upload', lazy=True, cascade='all, delete-orphan')


class Report(db.Model):
    """Generated report model."""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
