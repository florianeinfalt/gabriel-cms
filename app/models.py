from app import db
from flask.ext.login import UserMixin

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_live = db.Column(db.Boolean)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.email)
        except AttributeError:
            raise NotImplementedError('No `email` attribute - override `get_id`')

    def __repr__(self):
        return '<User {0}>'.format(self.name)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {0}>'.format(self.name)