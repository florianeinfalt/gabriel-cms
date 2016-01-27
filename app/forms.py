import string
from flask_wtf import Form
from wtforms import BooleanField, DateTimeField, DecimalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


### USER MANAGEMENT ########################################################

class LoginForm(Form):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=32, message='Password must be between 8 and 32 charcters long')])
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


### DATA MANAGEMENT ########################################################

class QualificationFormAdd(Form):
    name = StringField('Name', validators=[DataRequired(),
                                           Length(max=64, message='Name cannot be longer than 64 characters')])
    locale = SelectField('Locale')
    year = SelectField('Year')
    num_students = IntegerField('Number of Students', default=0)
    submit = SubmitField('Add Qualification')

class SubjectFormAdd(Form):
    qualification = SelectField(validators=[DataRequired()], coerce=int)
    board = SelectField(validators=[DataRequired()], coerce=int)
    name = StringField('Name', validators=[DataRequired(),
                                           Length(max=64, message='Name cannot be longer than 64 characters')])
    is_compulsory = BooleanField('Compulsory?', default=False)
    is_higher = BooleanField('Higher?', default=False)
    perc_exam = DecimalField('Percentage Exam vs. Coursework', validators=[NumberRange(min=0.0,
                                                                                       max=1.0,
                                                                                       message='Fraction needs to be between 0.0 and 1.0')],
                                                                                       default=0.5)
    total_marks = IntegerField('Total Marks', default=0)
    num_modules = IntegerField('Number of Modules', default=0)
    num_students = IntegerField('Number of Students', default=0)
    submit = SubmitField('Add Subject')

class BoardFormAdd(Form):
    name = StringField('Name', validators=[DataRequired(),
                                           Length(max=64, message='Name cannot be longer than 64 characters')])
    locale = SelectField('Locale')
    num_marking = IntegerField('Number of Marking', default=0)
    submit = SubmitField('Add Board')

class ExamFormAdd(Form):
    subject = SelectField(validators=[DataRequired()], coerce=int)
    name = StringField('Name', validators=[DataRequired(),
                                           Length(max=64, message='Name cannot be longer than 64 characters')])
    marks = IntegerField('Number of Marks', default=0)
    total_num_q = IntegerField('Total number of Questions', default=0)
    required_num_q = IntegerField('Required number of Questions', default=0)
    time = IntegerField('Time in Minutes', default=0)
    datetime = DateTimeField()
    num_retakes = IntegerField('Number of Retakes', default=0)
    submit = SubmitField('Add Exam')

class SectionFormAdd(Form):
    exam = SelectField(validators=[DataRequired()], coerce=int)
    topic = StringField('Name', validators=[DataRequired()])
    marks = IntegerField('Number of Marks', default=0)
    time = IntegerField('Time in Minutes', default=0)
    submit = SubmitField('Add Section')

class QuestionFormAdd(Form):
    section = SelectField(validators=[DataRequired()], coerce=int)
    marks = IntegerField('Number of Marks', default=0)
    time = IntegerField('Time in Minutes', default=0)
    text = TextAreaField('Text', validators=[DataRequired()])
    meta = None
    submit = SubmitField('Add Question')