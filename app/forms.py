from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(Form):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login_button = SubmitField('Login')

class RegisterForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password', message='Passwords must match')])
    register_button = SubmitField('Register')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(),])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired(),
                                                                             EqualTo('new_password', message='Passwords must match')])
    change_password_button = SubmitField('Change Password')