from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app import db
from app.forms import RegisterForm, LoginForm, ServiceForm
from app.models import User, Service, StatusCheck
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(name=form.name.data, url=form.url.data, owner=current_user)
        db.session.add(service)
        db.session.commit()
        flash('Service added!', 'success')
    
    services = Service.query.filter_by(user_id=current_user.id).all()
    
    # Get latest status check for each service
    service_status = {}
    for service in services:
        last_check = StatusCheck.query.filter_by(service_id=service.id)\
            .order_by(StatusCheck.timestamp.desc()).first()
        service_status[service.id] = {
            'status': last_check.status_code if last_check else None,
            'response_time': last_check.response_time if last_check else None,
            'timestamp': last_check.timestamp if last_check else None,
            'error': last_check.error_message if last_check and last_check.status_code is None else None
        }
    
    return render_template('dashboard.html', 
                         services=services, 
                         service_status=service_status,
                         form=form)

@bp.route('/service/<int:service_id>')
@login_required
def service_details(service_id):
    service = Service.query.get_or_404(service_id)
    # Ensure user owns this service
    if service.user_id != current_user.id:
        abort(403)
    
    # Get last 24 hours of status checks
    status_checks = StatusCheck.query.filter_by(service_id=service_id)\
        .order_by(StatusCheck.timestamp.desc())\
        .limit(50)\
        .all()
    
    # Calculate uptime percentage
    successful_checks = [c for c in status_checks if c.status_code and c.status_code < 400]
    uptime_percent = len(successful_checks) / len(status_checks) * 100 if status_checks else 0
    
    return render_template('service_details.html',
                         service=service,
                         status_checks=status_checks,
                         uptime_percent=round(uptime_percent, 2))
