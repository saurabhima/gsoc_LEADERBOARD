from flask import Flask, request, redirect, url_for, flash, session
from flask.templating import render_template
import config
import sub_process
import pickle
import os
import datetime

app = Flask(__name__)
app.secret_key = 'abc1234'
app.config['DEBUG'] = True


# Default Index and testing Pages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/default')
def default():
    return render_template('default_testing.html')


#  Donor Leader Board Page
@app.route('/donorleaderboard')
def donor_leaderboard():
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    pickle_obj = None
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        print(pickle_obj)
    return render_template('donor_leaderboard.html', donor_list=pickle_obj)


# User Management Sub Modules

# New User Registration
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
    user['register_date'] = datetime.datetime.now().date().strftime("%m-%d-%Y")
    user['account_status'] = 'Pending'
    user_list.append(user)
    with open(user_details_pickle_filename, 'wb') as wfp:
        pickle.dump(user_list, wfp)
    log_str = 'New User Register:Username#' + username + '***Name#' + name + '***Account_Type#' + user_type + '***Register_Date#' + datetime.datetime.now().date().strftime(
        "%Y-%m-%d")
    sub_process.write_user_log(log_str)
    flash('Your User Credentials have been sent for verification to Administrator')
    return redirect(url_for('index'))


# User Login and Verification
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
    if logged_user_status is False:
        return render_template('default_testing.html')
    else:
        session['logged_username'] = username
        session['logged_user_type'] = logged_user_type
        session['logged_user_status'] = logged_user_status
        session['logged_user_full_name'] = user_fullname
        session['login_status'] = 'True'
        return redirect(url_for('index'))


# User Logout
@app.route('/logout')
def logout():
    session.pop('logged_username', None)
    session.pop('logged_user_type', None)
    session.pop('logged_user_status', None)
    session.pop('logged_user_full_name', None)
    session['login_status'] = 'False'
    return redirect(url_for('index'))


# Approve New User
@app.route('/approve_new_user')
def approve_new_user():
    user_list = sub_process.get_pending_user_list()
    if len(user_list) > 0:
        return render_template('approve_user.html', user=user_list[0])
    else:
        return redirect(url_for('index'))


@app.route('/approve_new_user_process', methods=['POST'])
def approve_new_user_process():
    print 'user approval process module'
    username = request.form['username']
    if request.form['submit'] == 'Approve':
        sub_process.approve_user(username)
        print 'User Approved'
        return redirect(url_for('approve_new_user'))
    else:
        sub_process.reject_user(username)
        print 'User Rejected'
        return redirect(url_for('approve_new_user'))


# Donor Management Sub Modules

# Register New Donor to Database
@app.route('/register_new_donor')
def register_new_donor():
    try:
        if session['login_status'] == 'True' and (
                        session['logged_user_type'] == 'Administrator' or session['logged_user_type'] == 'Supervisor'):
            return render_template('register_new_donor.html')
        else:
            return render_template('invalid_login.html')
    except:

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
    anonymous_select = request.form['anonymous_select']
    donor_list = []
    donor_pickle_filename = 'donor_details.pickle'
    donor_list_len = 0
    if os.path.exists(donor_pickle_filename):
        with open(donor_pickle_filename, 'rb') as rfp:
            donor_list = pickle.load(rfp)
            donor_list_len = len(donor_list)
    donor = {}
    donor['id'] = donor_list_len + 1
    donor['title'] = title
    donor['name'] = name
    donor['org'] = org
    donor['phone'] = donor_contact
    donor['email'] = email
    donor['contact_person'] = contact_person
    donor['contact_date'] = contact_date
    donor['anonymous_select'] = anonymous_select
    donor['donor_status'] = 'New'
    donor_list.append(donor)
    with open(donor_pickle_filename, 'wb') as wfp:
        pickle.dump(donor_list, wfp)
    return redirect(url_for('index'))


# Donor Phone Contact
@app.route('/donor_phone_contact')
def donor_phone_contact():
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    pickle_obj = None
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
    return render_template('donor_phone_contact.html', donor_list=pickle_obj)


@app.route('/donor_phone_contact_process', methods=['POST'])
def donor_phone_contact_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_previous_logs = sub_process.donor_contact_logs_byid(donor_id)
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    return render_template('donor_phone_contact_logging.html', donor_obj=donor_obj, contact_log=donor_previous_logs,
                           current_date=current_date, current_time=current_time)


@app.route('/donor_phone_log_process', methods=['POST'])
def donor_phone_log_process():
    contact_person = request.form['contact_person']
    donor_id = request.form['donor_id']
    contact_date = request.form['contact_date']
    contact_time = request.form['contact_time']
    details_shared = request.form['details_shared']
    remarks = request.form['remarks']
    donor_log = {}
    donor_log['donor_id'] = donor_id
    donor_log['contact_person'] = contact_person
    donor_log['contact_date'] = contact_date
    donor_log['contact_time'] = contact_time
    donor_log['contact_mode'] = 'Phone'
    donor_log['details_shared'] = details_shared
    donor_log['remarks'] = remarks
    sub_process.add_donor_log(donor_log)
    return redirect(url_for('donor_phone_contact'))


# Main Function Call
if __name__ == '__main__':
    app.run()
