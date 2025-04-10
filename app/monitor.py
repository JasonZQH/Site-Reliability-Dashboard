from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from app.models import Service, StatusCheck
from app.extensions import db
import requests
from datetime import datetime

scheduler = BackgroundScheduler()

def check_service(service):
    """Check a single service and record its status"""
    try:
        start_time = datetime.utcnow()
        response = requests.get(service.url, timeout=10)
        end_time = datetime.utcnow()
        
        status_check = StatusCheck(
            service_id=service.id,
            status_code=response.status_code,
            response_time=(end_time - start_time).total_seconds(),
            timestamp=end_time
        )
        
        try:
            db.session.add(status_check)
            db.session.commit()
        except Exception as db_error:
            db.session.rollback()
            current_app.logger.error(f"Database error recording status for {service.name}: {str(db_error)}")
        
    except requests.exceptions.RequestException as e:
        status_check = StatusCheck(
            service_id=service.id,
            status_code=None,
            response_time=None,
            error_message=str(e),
            timestamp=datetime.utcnow()
        )
        try:
            db.session.add(status_check)
            db.session.commit()
        except Exception as db_error:
            db.session.rollback()
            current_app.logger.error(f"Database error recording failed status for {service.name}: {str(db_error)}")

def check_all_services(app):
    """Check all registered services"""
    with app.app_context():
        services = Service.query.all()
        for service in services:
            check_service(service)

def start_scheduler(app):
    """Start the monitoring scheduler"""
    if not scheduler.running:
        interval = app.config.get('MONITOR_INTERVAL', 5)
        scheduler.add_job(
            func=lambda: check_all_services(app),
            trigger='interval',
            minutes=interval,
            id='service_monitor'
        )
        scheduler.start()
        app.logger.info(f"Started service monitor with {interval} minute interval")
