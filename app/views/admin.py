from app import app, db, utilities
from app.models import User
from flask import render_template, request, url_for
from flask_sqlalchemy import Pagination
from flask.ext.login import current_user, login_required


@app.route('/admin/users/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/admin/users/page/<int:page>', methods=['GET', 'POST'])
@login_required
def admin_users(page):
    if request.method == 'POST':
        if 'submit' in request.form:
            command = request.form['submit'].split('-')[0]
            email = request.form['submit'].split('-')[1]
            if command == 'disable':
                User.query.filter_by(email=email).first().is_live = False
                db.session.commit()
            elif command == 'enable':
                User.query.filter_by(email=email).first().is_live = True
                db.session.commit()

    query = User.query.all
    count = len(query())
    users = utilities.get_items_for_page(query, page)
    table_header = ['ID', 'Name', 'Email Address', 'Role', 'Is Live?', 'Enable/Disable']
    table_data = [[str(user.id), user.name, user.email, user.role.name, user.is_live] for user in users]
    if not users and page != 1:
        abort(404)
    pagination = Pagination(query(), page, app.config['PER_PAGE'], count, users)
    return render_template('admin_users.html',
                           user=current_user.name,
                           user_role=current_user.role.name,
                           all_users_header=table_header,
                           all_users_list=table_data,
                           pagination=pagination)