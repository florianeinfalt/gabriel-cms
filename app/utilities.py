import re
from app import app
from flask import flash, request, url_for


def password_is_valid(password):
    if len(password) >= 8 and len(password) <= 32 and \
       ' ' not in password and \
       re.search(r'[A-Z]', password) and \
       re.search(r'[a-z]', password) and \
       re.search(r'[0-9]', password):
        return True
    return False


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def url_for_this_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_this_page'] = url_for_this_page


def get_items_for_page(query, page, per_page=app.config['PER_PAGE']):
    min_range = (page - 1) * per_page
    max_range = min_range + per_page
    return query()[min_range:max_range]


def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('Error in the {0} field - {1}'.format(getattr(form, field).label.text, error), 'error')