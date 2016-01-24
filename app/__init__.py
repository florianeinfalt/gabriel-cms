from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager

from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    Bootstrap(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return app, db, migrate, manager

# Create App (-> APP, DB)
app, db, migrate, manager = create_app('development')

# Import DB models
from app.models import User
# import defaults

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()

from app.views import admin, index, userhandler


