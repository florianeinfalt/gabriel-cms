from app import app, db, utilities
from app.forms import QualificationFormAdd, SubjectFormAdd, BoardFormAdd, ExamFormAdd, SectionFormAdd, QuestionFormAdd
from app.models import Qualification, Subject, Board, Exam, Section, Question
from flask import abort, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user
from flask_sqlalchemy import Pagination


import json
import random

@app.route('/data')
def data():
    table_data = [
        ['Qualifications', len(Qualification.query.all())],
        ['Subjects', len(Subject.query.all())],
        ['Boards', len(Board.query.all())],
        ['Exams', len(Exam.query.all())],
        ['Sections', len(Section.query.all())],
        ['Questions', len(Question.query.all())]]
    graph_data = []
    cat_labels = [cat[0] for cat in table_data]
    primary_color_list = [('#F7464A', '#FF5A5E'), ('#46BFBD', '#5AD3D1'), ('#FDB45C', '#FFC870'), ('#949FB1', '#A8B3C5')]
    secondary_color_list =  [('#4D5360', '#616774'), ('#5C5CF8', '#6E6EFF'), ('#C4F85C', '#CFFF6E')]
    for label in cat_labels:
        if primary_color_list:
            color = random.choice(primary_color_list)
            primary_color_list.remove(color)
        else:
            color = random.choice(secondary_color_list)
            secondary_color_list.remove(color)
        graph_data.append({'label': label, 'value': round(random.random(), 3), 'color': color[0], 'highlight': color[1]})

    return render_template('data.html',
                           user=current_user.name,
                           user_role=current_user.role.name,
                           table_data=table_data,
                           graph_data=json.dumps(sorted(graph_data, key=lambda x: x['label'])))

@app.route('/data/entry', methods=['GET', 'POST'])
def data_entry():
    import pprint
    pprint.pprint(request.form)
    qualifications_form = QualificationFormAdd()
    qualifications_form.locale.choices = [('GB', 'GB'), ('DE', 'DE'), ('US', 'US')]
    qualifications_form.year.choices = [('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011')]
    board_form = BoardFormAdd()
    board_form.locale.choices = [('GB', 'GB'), ('DE', 'DE'), ('US', 'US')]
    subject_form = SubjectFormAdd()
    subject_form.qualification.choices = [(q.id, '{0} ({1}, {2})'.format(q.name,
                                                                         q.locale,
                                                                         q.year)) \
                                           for q in Qualification.query.all() \
                                           if Qualification.query.all()]
    subject_form.board.choices = [(q.id, '{0} ({1})'.format(q.name,
                                                            q.locale)) \
                                   for q in Board.query.all() \
                                   if Board.query.all()]
    exam_form = ExamFormAdd()
    exam_form.subject.choices = [(q.id, '{0} ({1} {2} [{3}])'.format(q.name,
                                                                     q.qualification.name,
                                                                     q.qualification.year,
                                                                     q.board.name)) \
                                  for q in Subject.query.all() \
                                  if Subject.query.all()]
    section_form = SectionFormAdd()
    section_form.exam.choices = [(q.id, '{0} ({1} {2} {3} [{4}])'.format(q.name,
                                                                         q.subject.name,
                                                                         q.subject.qualification.name,
                                                                         q.subject.qualification.year,
                                                                         q.subject.board.name)) \
                                  for q in Exam.query.all() \
                                  if Exam.query.all()]
    question_form = QuestionFormAdd()
    question_form.section.choices = [(q.id, '{0} ({1} {2} {3} {4} [{5}])'.format(q.topic,
                                                                                 q.exam.name,
                                                                                 q.exam.subject.name,
                                                                                 q.exam.subject.qualification.name,
                                                                                 q.exam.subject.qualification.year,
                                                                                 q.exam.subject.board.name)) \
                                      for q in Section.query.all() \
                                      if Section.query.all()]
    if request.method == 'GET':
        return render_template('data_entry.html',
                               user=current_user.name,
                               user_role=current_user.role.name,
                               qualifications_form=qualifications_form,
                               subject_form=subject_form,
                               board_form=board_form,
                               exam_form=exam_form,
                               section_form=section_form,
                               question_form=question_form)
    if request.method == 'POST':
        if qualifications_form.validate_on_submit():
            new_qualification = Qualification(name=qualifications_form.name.data,
                                              locale=qualifications_form.locale.data,
                                              year=qualifications_form.year.data,
                                              num_students=qualifications_form.num_students.data)
            db.session.add(new_qualification)
            db.session.commit()
            flash('Added Qualification: {0} ({1}, {2})'.format(qualifications_form.name.data,
                                                               qualifications_form.locale.data,
                                                               qualifications_form.year.data))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(qualifications_form)
        if board_form.validate_on_submit():
            new_board = Board(name=board_form.name.data,
                              locale=board_form.locale.data,
                              num_marking=board_form.num_marking.data)
            db.session.add(new_board)
            db.session.commit()
            flash('Added Board: {0} ({1})'.format(board_form.name.data,
                                                  board_form.locale.data))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(board_form)
        if subject_form.validate_on_submit():
            new_subject = Subject(name=subject_form.name.data,
                                  qualification_id=subject_form.qualification.data,
                                  board_id=subject_form.board.data,
                                  is_compulsory=subject_form.is_compulsory.data,
                                  is_higher=subject_form.is_higher.data,
                                  perc_exam=subject_form.perc_exam.data,
                                  total_marks=subject_form.total_marks.data,
                                  num_modules=subject_form.num_modules.data,
                                  num_students=subject_form.num_students.data)
            db.session.add(new_subject)
            db.session.commit()
            flash('Added Subject: {0} ({1} {2} [{3}])'.format(new_subject.name,
                                                              new_subject.qualification.name,
                                                              new_subject.qualification.year,
                                                              new_subject.board.name))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(subject_form)
        return redirect(url_for('data_entry'))

"""
@app.route('/data/qualifications/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/data/qualifications/page/<int:page>', methods=['GET', 'POST'])
def qualifications(methods=['GET', 'POST']):
    if request.method == 'POST':
        pass
    table_data = []
    return render_template('data.html',
                           user=current_user.name,
                           user_role=current_user.role.name,
                           table_data=table_data)
"""







