from app import app, db, utilities
from app.forms import QualificationFormAdd, SubjectFormAdd, BoardFormAdd, ExamFormAdd, SectionFormAdd, QuestionFormAdd
from app.forms import QualificationFormEdit
from app.models import Qualification, Subject, Board, Exam, Section, Question
from flask import abort, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user
from flask_sqlalchemy import Pagination


import json
import random

@app.route('/data')
def data():
    target_data = [
        ['Qualifications', 5],
        ['Subjects', 3],
        ['Boards', 2],
        ['Exams', 25],
        ['Sections', 50],
        ['Questions', 200]]
    table_data = [
        ['Qualifications', len(Qualification.query.all())],
        ['Subjects', len(Subject.query.all())],
        ['Boards', len(Board.query.all())],
        ['Exams', len(Exam.query.all())],
        ['Sections', len(Section.query.all())],
        ['Questions', len(Question.query.all())]]
    graph_data = []
    cat_labels = [cat[0] for cat in table_data]
    cat_values = [cat[1] for cat in table_data]
    target_values = [val[1] for val in target_data]
    primary_color_list = [('#F7464A', '#FF5A5E'), ('#46BFBD', '#5AD3D1'), ('#FDB45C', '#FFC870'), ('#949FB1', '#A8B3C5')]
    secondary_color_list =  [('#4D5360', '#616774'), ('#5C5CF8', '#6E6EFF'), ('#C4F85C', '#CFFF6E')]
    for idx, label in enumerate(cat_labels):
        if primary_color_list:
            color = random.choice(primary_color_list)
            primary_color_list.remove(color)
        else:
            color = random.choice(secondary_color_list)
            secondary_color_list.remove(color)
        graph_data.append({'label': label,
                           'value': round(cat_values[idx] / float(target_values[idx]), 3),
                           'color': color[0],
                           'highlight': color[1]})

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
    exam_form = ExamFormAdd()
    section_form = SectionFormAdd()
    question_form = QuestionFormAdd()
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
            flash('Added Qualification: {0} {1} ({2})'.format(new_qualification.name,
                                                              new_qualification.year,
                                                              new_qualification.locale))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(qualifications_form)
        if board_form.validate_on_submit():
            new_board = Board(name=board_form.name.data,
                              locale=board_form.locale.data,
                              num_marking=board_form.num_marking.data)
            db.session.add(new_board)
            db.session.commit()
            flash('Added Board: {0} ({1})'.format(new_board.name,
                                                  new_board.locale))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(board_form)
        if subject_form.validate_on_submit():
            new_subject = Subject(name=subject_form.name.data,
                                  qualification_id=subject_form.qualification.data.id,
                                  board_id=subject_form.board.data.id,
                                  is_compulsory=subject_form.is_compulsory.data,
                                  is_higher=subject_form.is_higher.data,
                                  perc_exam=subject_form.perc_exam.data,
                                  total_marks=subject_form.total_marks.data,
                                  num_modules=subject_form.num_modules.data,
                                  num_students=subject_form.num_students.data)
            db.session.add(new_subject)
            db.session.commit()
            flash('Added Subject: {0} | {1} {2} | {3} ({4})'.format(new_subject.name,
                                                                    new_subject.qualification.name,
                                                                    new_subject.qualification.year,
                                                                    new_subject.board.name,
                                                                    new_subject.board.locale))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(subject_form)
        if exam_form.validate_on_submit():
            new_exam = Exam(subject_id=exam_form.subject.data.id,
                            name=exam_form.name.data,
                            marks=exam_form.marks.data,
                            total_num_q=exam_form.total_num_q.data,
                            required_num_q=exam_form.required_num_q.data,
                            time=exam_form.time.data,
                            datetime=exam_form.datetime.data,
                            num_retakes=exam_form.num_retakes.data)
            db.session.add(new_exam)
            db.session.commit()
            flash('Added Exam: {0} | {1} | {2} {3} | {4} ({5})'.format(new_exam.name,
                                                                       new_exam.subject.name,
                                                                       new_exam.subject.qualification.name,
                                                                       new_exam.subject.qualification.year,
                                                                       new_exam.subject.board.name,
                                                                       new_exam.subject.board.locale))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(exam_form)
        if section_form.validate_on_submit():
            new_section = Section(exam_id=section_form.exam.data.id,
                                  topic=section_form.topic.data,
                                  marks=section_form.marks.data,
                                  time=section_form.time.data)
            db.session.add(new_section)
            db.session.commit()
            flash('Added Section: {0} | {1} | {2} | {3} {4} | {5} ({6})'.format(new_section.topic,
                                                                                new_section.exam.name,
                                                                                new_section.exam.subject.name,
                                                                                new_section.exam.subject.qualification.name,
                                                                                new_section.exam.subject.qualification.year,
                                                                                new_section.exam.subject.board.name,
                                                                                new_section.exam.subject.board.locale))
            return redirect(url_for('data_entry'))
        else:
            utilities.flash_form_errors(section_form)
        return redirect(url_for('data_entry'))


@app.route('/data/qualifications/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/data/qualifications/page/<int:page>', methods=['GET', 'POST'])
def qualifications(page):
    if request.method == 'POST':
        if 'submit' in request.form:
            command = request.form['submit'].split('-')[0]
            id = request.form['submit'].split('-')[1]
            if command == 'edit':
                redirect(url_for('qualifications'))
            elif command == 'delete':
                item = Qualification.query.filter_by(id=id).first()
                db.session.delete(item)
                db.session.commit()
    query = Qualification.query.order_by(Qualification.name, Qualification.year).all
    count = len(query())
    qualifications = utilities.get_items_for_page(query, page)
    table_header = ['ID', 'Name', 'Locale', 'Year', 'Number of Students', 'Actions']
    table_data = [[str(q.id), q.name, q.locale, q.year, q.num_students] for q in qualifications]
    if not qualifications and page != 1:
        abort(404)
    pagination = Pagination(query(), page, app.config['PER_PAGE'], count, qualifications)
    return render_template('data_display.html',
                           user=current_user.name,
                           user_role=current_user.role.name,
                           table_header=table_header,
                           table_data=table_data,
                           pagination=pagination)

@app.route('/data/qualifications/<int:id>', methods=['GET', 'POST'])
def qualification(id):
    """
    WIP
    """
    item = Qualification.query.filter_by(id=id).first()
    if not item:
        abort(404)
    qualifications_form = QualificationFormEdit()
    qualifications_form.locale.choices = [('GB', 'GB'), ('DE', 'DE'), ('US', 'US')]
    qualifications_form.year.choices = [('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011')]
    qualifications_form.i_d.data = item.id
    qualifications_form.name.data = item.name
    qualifications_form.locale.data = item.locale
    qualifications_form.year.data = item.year
    qualifications_form.num_students.data = item.num_students
    return render_template('data_edit.html',
                           user=current_user.name,
                           user_role=current_user.role.name,
                           form=qualifications_form)







