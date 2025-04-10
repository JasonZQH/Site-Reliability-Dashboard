"""
Database Models Definition
Defines all database tables and relationships using SQLAlchemy ORM
"""

from datetime import datetime
from app.extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback
    Loads user from database by ID"""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User account model"""
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials
    email = db.Column(db.String(120), unique=True, nullable=False)  # Must be unique
    password = db.Column(db.String(128), nullable=False)  # Hashed password storage
    
    # Relationship to services (one-to-many)
    services = db.relationship('Service', backref='owner', lazy=True)

class Service(db.Model):
    """Monitored service model"""
    __tablename__ = 'services'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Service details
    name = db.Column(db.String(100), nullable=False)  # Display name
    url = db.Column(db.String(200), nullable=False)   # Endpoint to monitor
    
    # Foreign key to owner user (matches User.__tablename__)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamp of creation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StatusCheck(db.Model):
    """Service status check history"""
    __tablename__ = 'status_checks'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to service (matches Service.__tablename__)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    # Check results
    status_code = db.Column(db.Integer)       # HTTP status code or None if failed
    response_time = db.Column(db.Float)       # Response time in seconds
    error_message = db.Column(db.String(200)) # Error details if request failed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When check occurred
