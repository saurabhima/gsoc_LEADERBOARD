from flask import request, redirect, url_for, flash, session
from flask.templating import render_template
import config
import sub_process
import pickle
import os
import datetime

from leaderboard import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/default')
def default():
    return render_template('default_testing.html')


#  Donor Leader Board Page
@app.route('/donorleaderboard')
def donor_leaderboard():
    donors = sub_process.get_donor_list()
    return render_template('donor_leaderboard.html', donor_list=donors)


# User Management Sub Modules

# New User Registration
@app.route('/user_register')
def user_register():
    return render_template('register_new_user.html')


@app.route('/process_new_user_register', methods=['POST'])
def process_new_user_register():
    name = request.form['user_full_name']
    email = request.form['user_email']
    user_contact = request.form['user_contact']
    username = request.form['username']
    password = request.form['user_password']
    user_type = request.form['user_type']
    # print (name, email, user_contact, username, password, user_type)
    if name and email and username and password and user_type:
        sub_process.add_user_details_db(name=name,email=email,user_contact=user_contact,username=username,password=password,user_type=user_type)
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
    # print (username, password)
    logged_user_status, logged_user_type, user_fullname = sub_process.authenticate(username, password)
    print (logged_user_type, logged_user_status, user_fullname)
    if logged_user_status is False:
        return render_template('default_testing.html')
    else:
        session['logged_username'] = username
        session['logged_user_type'] = logged_user_type
        session['logged_user_status'] = logged_user_status
        session['logged_user_full_name'] = user_fullname
        return redirect(url_for('index'))


# User Logout
@app.route('/logout')
def logout():
    session.pop('logged_username', None)
    session.pop('logged_user_type', None)
    session.pop('logged_user_status', None)
    session.pop('logged_user_full_name', None)
    return redirect(url_for('index'))


# Approve New User
@app.route('/approve_new_user')
def approve_new_user():
    user_list = sub_process.get_pending_user_list()
    if user_list:
        user = user_list[0]
        user.user_type = str(list(user.user_type)[0])
        user.phone = int(user.phone)
        return render_template('approve_user.html', user=user)
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
    if 'logged_user_type' in session and session['logged_user_type'] in ['Administrator', 'Supervisor']:
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
    contact_date = datetime.datetime.strptime(contact_date, '%m/%d/%Y')
    anonymous_select = request.form['anonymous_select']
    sub_process.register_new_donor(title=title,name=name,org=org,email=email,
                                   donor_contact=donor_contact,contact_person=contact_person,
                                   contact_date=contact_date,anonymous_select=anonymous_select)
    return redirect(url_for('index'))


# Update Donor Contacts
@app.route('/donor_contact_update')
def donor_contact_update():
    donor_list = sub_process.get_donor_list()
    return render_template('donor_contact_update.html', donor_list=donor_list)


@app.route('/donor_contact_update_process', methods=['POST'])
def donor_contact_update_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    return render_template('donor_contact_update_form.html', donor_obj=donor_obj)


@app.route('/donor_contact_update_form_process', methods=['POST'])
def donor_contact_update_form_process():
    donor_id = request.form['donor_id']
    phone = request.form['donor_contact']
    email = request.form['donor_email']
    sub_process.update_donor_contact(donor_id=donor_id, phone=phone, email=email)
    return redirect(url_for('donor_contact_update'))


# Donor Phone Contact
@app.route('/donor_phone_contact')
def donor_phone_contact():
    donor_list = sub_process.get_donor_list()
    return render_template('donor_phone_contact.html', donor_list=donor_list)


@app.route('/donor_phone_contact_process', methods=['POST'])
def donor_phone_contact_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_obj.donor_status = str(list(donor_obj.donor_status)[0])
    donor_previous_phone_logs = sub_process.donor_phone_logs_byid(donor_id)
    donor_previous_email_logs = sub_process.donor_email_logs_byid(donor_id)
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    return render_template('donor_phone_contact_logging.html', donor_obj=donor_obj, phone_log=donor_previous_phone_logs,
                           email_log=donor_previous_email_logs,
                           current_date=current_date, current_time=current_time)


@app.route('/donor_phone_log_process', methods=['POST'])
def donor_phone_log_process():
    contact_person = request.form['contact_person']
    donor_id = request.form['donor_id']
    contact_date = request.form['contact_date']
    print contact_date
    contact_date = datetime.datetime.strptime(contact_date, '%m-%d-%Y')
    contact_time = request.form['contact_time']
    details_shared = request.form['details_shared']
    remarks = request.form['remarks']
    sub_process.add_donor_phone_log(donor_id=donor_id,contact_person=contact_person,contact_date=contact_date,
                                     contact_time=contact_time,details_shared=details_shared,remarks=remarks)

    return redirect(url_for('donor_phone_contact'))


@app.route('/donor_email_contact')
def donor_email_contact():
    donors = sub_process.get_donor_list()
    return render_template('donor_email_contact.html', donor_list=donors)


@app.route('/donor_email_contact_process', methods=['POST'])
def donor_email_contact_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_previous_phone_logs = sub_process.donor_phone_logs_byid(donor_id)
    donor_previous_email_logs = sub_process.donor_email_logs_byid(donor_id)
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    return render_template('donor_email_contact_logging.html', donor_obj=donor_obj, phone_log=donor_previous_phone_logs,
                           email_log=donor_previous_email_logs,
                           current_date=current_date, current_time=current_time)


@app.route('/allot_volunteer')
def allot_volunteer():
    donor_list = sub_process.get_new_donor_list()
    volunteer_list = sub_process.get_volunteer_list()
    if len(donor_list) > 0:
        return render_template('donor_volunteer_allot.html', donor=donor_list[0], volunteers=volunteer_list)
    else:
        return redirect(url_for('index'))


@app.route('/allot_volunteer_process', methods=['POST'])
def allot_volunteer_process():
    donor_id = request.form['donor_id']
    volunteer_name = request.form['volunteer_name']
    sub_process.allot_volunteer(donor_id, volunteer_name)
    return redirect(url_for('allot_volunteer'))


@app.route('/commit_donation')
def commit_donation():
    donor_list = sub_process.allotted_donors_byid(session['logged_user_full_name'])
    return render_template('commit_donation.html', donor_list=donor_list)


@app.route('/commit_donation_process', methods=['POST'])
def commit_donation_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_previous_phone_logs = sub_process.donor_phone_logs_byid(donor_id)
    donor_previous_email_logs = sub_process.donor_email_logs_byid(donor_id)
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    return render_template('commit_donation_mode_amt.html', donor_obj=donor_obj, phone_log=donor_previous_phone_logs,
                           email_log=donor_previous_email_logs,
                           current_date=current_date, current_time=current_time)


@app.route('/commit_donation_amt_process', methods=['POST'])
def commit_donation_amt_process():
    donor_id = request.form['donor_id']
    commit_date = request.form['commit_date']
    commit_time = request.form['commit_time']
    commit_amt = request.form['committed_amt']
    currency = request.form['currency']
    payment_mode = request.form['payment_mode']
    remarks = request.form['remarks']
    donation_details = {}
    donation_details['donor_id'] = donor_id
    donation_details['commit_date'] = commit_date
    donation_details['commit_time'] = commit_time
    donation_details['commit_amt'] = commit_amt
    donation_details['currency'] = currency
    donation_details['payment_mode'] = payment_mode
    donation_details['remarks'] = remarks
    sub_process.commit_donation(donation_details)
    return redirect(url_for('index'))
