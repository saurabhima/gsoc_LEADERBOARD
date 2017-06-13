import flask
from flask import Flask, request, redirect, url_for, get_flashed_messages, flash, session
from flask.templating import render_template
import config, sub_process
import pickle
import os
import datetime

app = Flask(__name__)
app.secret_key = 'abc1234'
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/default')
def default():
    return render_template('default_testing.html')


@app.route('/donorleaderboard')
def donor_leaderboard():
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    pickle_obj = None
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        print(pickle_obj)
    return render_template('donor_leaderboard.html', donor_list=pickle_obj)


@app.route('/user_register')
def user_register():
    return render_template('register_new_user.html')


@app.route('/process_new_user_register', methods=['POST'])
def process_new_user_register():
    print 'hello'

    name = request.form['user_full_name']
    email = request.form['user_email']
    user_contact = request.form['user_contact']
    username = request.form['username']
    password = request.form['user_password']
    user_type = request.form['user_type']
    print (name, email, user_contact, username, password, user_type)
    user_list = []
    user_details_pickle_filename = config.USER_DETAILS_PICKLE_FILE

    if os.path.exists(user_details_pickle_filename):
        with open(user_details_pickle_filename, 'rb') as rfp:
            user_list = pickle.load(rfp)

    user = {}

    user['name'] = name

    user['phone'] = user_contact
    user['email'] = email
    user['username'] = username
    user['password'] = password
    user['user_type'] = user_type
    user['register_date'] = datetime.datetime.now().date().strftime("%Y-%m-%d")
    user['account_status'] = 'Pending'
    user_list.append(user)

    with open(user_details_pickle_filename, 'wb') as wfp:
        pickle.dump(user_list, wfp)

    log_str = 'New User Register:Username#' + username + '***Name#' + name + '***Account_Type#' + user_type + '***Date_of_Registration#' + datetime.datetime.now().date().strftime(
        "%Y-%m-%d")
    sub_process.write_user_log(log_str)
    flash('Your User Credentials have been sent for verification to Administrator')
    return redirect(url_for('index'))


@app.route('/user_login')
def user_login():
    return render_template('user_login.html')


@app.route('/user_login_process', methods=['POST'])
def user_login_process():
    print 'user login process module'
    username = request.form['username']
    password = request.form['user_password']
    print (username, password)
    logged_user_status, logged_user_type, user_fullname = sub_process.authenticate(username, password)
    print (logged_user_type, logged_user_status, user_fullname)
    if logged_user_status == False:
        return render_template('default_testing.html')
    else:
        session['logged_username'] = username
        session['logged_user_type'] = logged_user_type
        session['logged_user_status'] = logged_user_status
        session['logged_user_full_name'] = user_fullname
        session['login_status'] = 'True'
        return redirect(url_for('index'))


@app.route('/register_new_donor')
def register_new_donor():
    if session['login_status'] == 'True' and (
            session['logged_user_type'] == 'Administrator' or session['logged_user_type'] == 'Supervisor'):
        return render_template('register_new_donor.html')
    else:
        return render_template('invalid_login.html')


@app.route('/process_donor_form', methods=['POST'])
def process_add_donors():
    title = request.form['donor_title']
    name = request.form['donor_name']
    org = request.form['donor_org']
    email = request.form['donor_email']

    donor_contact = request.form['donor_contact']
    contact_person = request.form['contact_person']
    contact_date = request.form['contact_date']
    donor_list = []
    donor_pickle_filename = 'donor_details.pickle'

    if os.path.exists(donor_pickle_filename):
        with open(donor_pickle_filename, 'rb') as rfp:
            donor_list = pickle.load(rfp)
    donor = {}
    donor['title'] = title
    donor['name'] = name
    donor['org'] = org

    donor['phone'] = donor_contact
    donor['email'] = email
    donor['contact_person'] = contact_person
    donor['contact_date'] = contact_date
    donor_list.append(donor)

    with open(donor_pickle_filename, 'wb') as wfp:
        pickle.dump(donor_list, wfp)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('logged_username', None)
    session.pop('logged_user_type', None)
    session.pop('logged_user_status', None)
    session.pop('logged_user_full_name', None)
    session['login_status'] = 'False'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
