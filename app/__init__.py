"""
Application Factory Pattern Implementation
Creates and configures the Flask application instance
"""

from flask import Flask
from config import Config
from app.extensions import db, login_manager
from app.monitor import start_scheduler, scheduler
from app.template_filters import datetimeformat
import atexit

# Set the login view endpoint for Flask-Login
# 'main.login' refers to the login route in the main blueprint
login_manager.login_view = 'main.login'  # redirect if not logged in

def create_app():
    """Application Factory Function"""
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize database and login manager with app
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register routes blueprint
    from app import routes
    app.register_blueprint(routes.bp)

    # Register custom template filters
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    # Start monitoring scheduler when app starts
    with app.app_context():
        # Pass app instance to scheduler to ensure proper context
        start_scheduler(app)  # Start background monitoring jobs with app context
        # Register shutdown handler to stop scheduler when app exits
        atexit.register(lambda: scheduler.shutdown())

    return app
