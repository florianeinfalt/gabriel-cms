from app import app
from flask.ext.login import login_required, current_user
from flask import render_template

@app.route('/')
@login_required
def index():
    return render_template('index.html',
                           user=current_user.name,
                           user_role=current_user.role.name)
