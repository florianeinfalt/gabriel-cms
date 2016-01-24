from app import app, db
from app.models import Role, User
from flask import redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    all_users = User.query.all()
    all_users_header = ['ID', 'Name', 'Email Address', 'Role', 'Is Live?', 'Enable/Disable']
    all_users_list = [[str(user.id), user.name, user.email, user.role.name, user.is_live] for user in all_users]
    if request.method == 'POST':
        if 'submit' in request.form:
            command = request.form['submit'].split('-')[0]
            email = request.form['submit'].split('-')[1]
            if command == 'disable':
                User.query.filter_by(email=email).first().is_live = False
                db.session.commit()
                return redirect(url_for('admin_users'))
            elif command == 'enable':
                User.query.filter_by(email=email).first().is_live = True
                db.session.commit()
                return redirect(url_for('admin_users'))

    return render_template('admin_users.html',
                           user=current_user.name,
                           user_role=current_user.role.name,
                           all_users_header=all_users_header,
                           all_users_list=all_users_list)