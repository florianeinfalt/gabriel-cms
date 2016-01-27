from app import app, db, utilities
from app.models import Role, User
from app.forms import RegisterForm, LoginForm, ChangePasswordForm

from flask import flash, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html',
                               register_form=register_form)
    if request.method == 'POST':
        if register_form.validate_on_submit():
            print register_form.password.data
            if User.query.filter_by(email=register_form.email.data).first():
                flash('This email address is already associated with an existing user account. User another email address.')
                return redirect(url_for('register'))
            if not utilities.password_is_valid(register_form.password.data):
                flash('Password is not strong enough.\nNeeds to contain lower case and upper case letters, numericals and punctuation.\nLength must be between 8 and 12 characters.')
                return redirect(url_for('register'))
            user_role = Role.query.filter_by(name='User').first()
            new_user = User(name=register_form.name.data,
                            email=register_form.email.data,
                            password=register_form.password.data,
                            role=user_role,
                            is_live=True)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',
                               login_form=login_form)
    if request.method == 'POST':
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if not user:
                flash('User {0} does not exist'.format(login_form.email.data))
                return redirect(url_for('login'))
            if not user.is_live:
                flash('User {0} is deactivated. Please contact an admin to reactivate'.format(login_form.email.data))
                return redirect(url_for('login'))
            if not user.verify_password(login_form.password.data):
                flash('Invalid password')
                return redirect(url_for('login'))
            if login_form.remember_me.data:
                login_user(user, remember=True)
            else:
                login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()
    if request.method == 'GET':
        return render_template('change_password.html',
                               user=current_user.name,
                               user_role=current_user.role.name,
                               change_password_form=change_password_form)
    if request.method == 'POST':
        if change_password_form.validate_on_submit():
            new_password = change_password_form.new_password.data
            old_password = change_password_form.old_password.data
            if not User.query.filter_by(email=current_user.email).first().verify_password(old_password):
                flash('Old password is invalid')
                return redirect(url_for('change_password'))
            if not utilities.password_is_valid(new_password):
                flash('Password is not strong enough.\nNeeds to contain lower case and upper case letters, numericals and punctuation.\nLength must be between 8 and 12 characters.')
                return redirect(url_for('change_password'))
            User.query.filter_by(email=current_user.email).first().password = new_password
            db.session.commit()
            flash('Password changed successfully')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('change_password'))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('login'))