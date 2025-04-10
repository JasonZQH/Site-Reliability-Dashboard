# Site Reliability Dashboard

A Flask web application for monitoring service uptime and performance metrics.

## Features

- ✅ Real-time service monitoring with configurable intervals
- ✅ User authentication (register/login)
- ✅ Dashboard showing service status and uptime percentages
- ✅ Detailed service history and response time tracking
- ✅ Background scheduler for automatic status checks
- ✅ Responsive web interface

## Technology Stack

- **Backend**: Python 3, Flask
- **Database**: SQLAlchemy ORM (PostgreSQL/SQLite)
- **Scheduler**: APScheduler
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Authentication**: Flask-Login

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sre-uptime-dashboard.git
cd sre-uptime-dashboard
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python run.py
```

6. Start the development server:
```bash
flask run
```

## Configuration

Set these environment variables in `.env`:
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
MONITOR_INTERVAL=5  # minutes between checks
```

## Usage

1. Access the application at `http://localhost:5001`
2. Register a new account
3. Add services to monitor via the dashboard
4. View uptime statistics and response history

## Project Structure

```
sre-uptime-dashboard/
├── app/                 # Application package
│   ├── __init__.py      # App factory
│   ├── models.py        # Database models
│   ├── routes.py        # View controllers  
│   ├── monitor.py       # Background monitoring
│   ├── templates/       # Jinja2 templates
│   └── static/          # Static assets
├── run.py               # Entry point
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## License

MIT License
