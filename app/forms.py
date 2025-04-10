from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, Length, URL

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    url = URLField('Service URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Service')
