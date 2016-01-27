import json
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()

class TextPickleType(db.PickleType):
    impl = db.Text

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_live = db.Column(db.Boolean)

    password_hash = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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


class Qualification(db.Model):
    __tablename__ = 'qualifications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    locale = db.Column(db.String(2))
    year = db.Column(db.Integer)
    num_students = db.Column(db.Integer)
    subjects = db.relationship('Subject', backref='qualification')

    def __repr__(self):
        return '<Qualification {0} ({1}) {2}>'.format(self.name, self.locale, self.year)


class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    locale = db.Column(db.String(2))
    num_marking = db.Column(db.Integer)
    subjects = db.relationship('Subject', backref='board')

    def __repr__(self):
        return '<Board {0} ({1})>'.format(self.name, self.locale)


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    qualification_id = db.Column(db.Integer, db.ForeignKey('qualifications.id'))
    name = db.Column(db.String(64), nullable=False)
    is_compulsory = db.Column(db.Boolean)
    is_higher = db.Column(db.Boolean)
    perc_exam = db.Column(db.Float)
    total_marks = db.Column(db.Integer)
    num_modules = db.Column(db.Integer)
    num_students = db.Column(db.Integer)
    exams = db.relationship('Exam', backref='subject')

    def __repr__(self):
        return '<Subject {0} ({1}, {2})>'.format(self.name, self.qualification.name, self.board.name)


class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    name = db.Column(db.String(64), nullable=False)
    marks = db.Column(db.Integer)
    total_num_q = db.Column(db.Integer)
    required_num_q = db.Column(db.Integer)
    time = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    num_retakes = db.Column(db.Integer)
    sections = db.relationship('Section', backref='exam')

    def __repr__(self):
        return '<Exam {0} ({1})>'.format(self.name, self.subject.name)


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    topic = db.Column(db.String, nullable=False)
    marks = db.Column(db.Integer)
    time = db.Column(db.Integer)
    questions = db.relationship('Question', backref='section')

    def __repr__(self):
        return '<Section {0} ({1} {2})>'.format(self.topic, self.exam.name, self.exam.subject.name)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    marks = db.Column(db.Integer)
    time = db.Column(db.Integer)
    text = db.Column(db.String, nullable=False)
    meta = db.Column(TextPickleType(pickler=json))


