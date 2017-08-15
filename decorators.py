from functools import wraps
from flask import session, render_template


def user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_status' in session and session['login_status'] == 'True' and (
            session['logged_user_type'] == 'Administrator' or session[
                'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):
            return f(*args, **kwargs)
        else:
            return render_template('invalid_login.html')

    return decorated_function


def privileged(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_status' in session and session['login_status'] == 'True' and (
                session['logged_user_type'] == 'Administrator' or session['logged_user_type'] == 'Supervisor'):
            return f(*args, **kwargs)
        else:
            return render_template('invalid_login.html')

    return decorated_function