from datetime import datetime

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object or timestamp string"""
    if value is None:
        return ''
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
    return value.strftime(format)
