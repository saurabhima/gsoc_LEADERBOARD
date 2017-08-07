from flask import request, redirect, url_for, session
from flask.templating import render_template
import config
import sub_process
import pickle
import os
import datetime
import json
from leaderboard import app
from forms import UserRegistrationForm, DonorContactUpdateForm, DonorAddForm, DonationCommitForm
from pprint import pprint

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
    form = UserRegistrationForm(request.form)

    if not form.validate():
        return redirect(url_for('user_register'))

    name = form.user_full_name.data
    email = form.user_email.data
    user_contact = form.user_contact.data
    username = form.username.data
    password = form.user_password.data
    user_type = form.user_type.data

    user_exists = sub_process.find_user_by_email(email) is not None or sub_process.find_user_by_username(
        username) is not None
    if user_exists:
        return redirect(url_for('user_register'))

    sub_process.add_user_details_db(name=name, email=email, user_contact=user_contact, username=username,
                                    password=password, user_type=user_type)

    # Module for Storing in Pickle File
    # user_list = []
    # user_details_pickle_filename = config.USER_DETAILS_PICKLE_FILE
    # if os.path.exists(user_details_pickle_filename):
    #     with open(user_details_pickle_filename, 'rb') as rfp:
    #         user_list = pickle.load(rfp)
    # user = {}
    # user['name'] = name
    # user['phone'] = user_contact
    # user['email'] = email
    # user['username'] = username
    # user['password'] = password
    # user['user_type'] = user_type
    # user['register_date'] = datetime.datetime.now().date().strftime("%m-%d-%Y")
    # user['account_status'] = 'Pending'
    # user_list.append(user)
    # with open(user_details_pickle_filename, 'wb') as wfp:
    #     pickle.dump(user_list, wfp)
    # log_str = 'New User Register:Username#' + username + '***Name#' +
    # name + '***Account_Type#' + user_type + '***Register_Date#' +
    #  datetime.datetime.now().date().strftime(
    #     "%Y-%m-%d")
    # sub_process.write_user_log(log_str)
    # flash('Your User Credentials have been sent for verification to Administrator')
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
        user = user_list[0]
        user.user_type = user.user_type
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
    form = DonorAddForm(request.form)

    if not form.validate():
        print form.errors
        return redirect(url_for('register_new_donor'))

    title = form.donor_title.data
    name = form.donor_name.data
    org = form.donor_org.data
    email = form.donor_email.data
    donor_contact = form.donor_contact.data
    contact_person = form.contact_person.data
    contact_date = form.contact_date.data
    anonymous_select = form.anonymous_select.data

    sub_process.register_new_donor(title=title, name=name, org=org, email=email,
                                   donor_contact=donor_contact, contact_person=contact_person,
                                   contact_date=contact_date, anonymous_select=anonymous_select)
    return redirect(url_for('index'))


# Update Donor Contacts
@app.route('/donor_contact_update')
def donor_contact_update():
    try:
        if session['login_status'] == 'True' and (
                            session['logged_user_type'] == 'Administrator' or session[
                        'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):
            donor_list = sub_process.get_donor_list()
            return render_template('donor_contact_update.html', donor_list=donor_list)

        else:
            return render_template('invalid_login.html')
    except:

        return render_template('invalid_login.html')


@app.route('/donor_contact_update_process', methods=['POST'])
def donor_contact_update_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    return render_template('donor_contact_update_form.html', donor_obj=donor_obj)


@app.route('/donor_contact_update_form_process', methods=['POST'])
def donor_contact_update_form_process():
    form = DonorContactUpdateForm(request.form)
    donor_id = request.form['donor_id']
    phone = form.donor_contact.data
    email = form.donor_email.data
    org = form.donor_org.data
    if not form.validate() or not sub_process.find_donor(donor_id):
        return redirect(url_for('donor_contact_update'))

    sub_process.update_donor_contact(donor_id=donor_id, phone=phone, email=email, org=org)
    return redirect(url_for('donor_contact_update'))


# Donor Phone Contact
@app.route('/donor_phone_contact')
def donor_phone_contact():
    try:
        if session['login_status'] == 'True' and (
                            session['logged_user_type'] == 'Administrator' or session[
                        'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):
            donor_list = sub_process.get_donor_list()
            return render_template('donor_phone_contact.html', donor_list=donor_list)

        else:
            return render_template('invalid_login.html')
    except:

        return render_template('invalid_login.html')


@app.route('/donor_phone_contact_process', methods=['POST'])
def donor_phone_contact_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_obj.donor_status = donor_obj.donor_status
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
    sub_process.add_donor_phone_log(donor_id=donor_id, contact_person=contact_person, contact_date=contact_date,
                                    contact_time=contact_time, details_shared=details_shared, remarks=remarks)

    return redirect(url_for('donor_phone_contact'))


@app.route('/send_email_indl_donor')
def send_email_indl_donor():
    try:
        if session['login_status'] == 'True' and (
                            session['logged_user_type'] == 'Administrator' or session[
                        'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):
            donor_list = sub_process.get_donor_list()
            return render_template('send_email_indl_donor.html', donor_list=donor_list)

        else:
            return render_template('invalid_login.html')
    except:

        return render_template('invalid_login.html')


@app.route('/send_email_indl_donor_process', methods=['POST'])
def send_email_indl_donor_process():
    donor_id = request.form['submit']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_previous_phone_logs = sub_process.donor_phone_logs_byid(donor_id)
    donor_previous_email_logs = sub_process.donor_email_logs_byid(donor_id)
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    email_template_list = sub_process.get_email_template_list()
    return render_template('send_email_indl_donor_logging.html', donor_obj=donor_obj,
                           phone_log=donor_previous_phone_logs,
                           email_log=donor_previous_email_logs,
                           current_date=current_date, current_time=current_time,
                           email_template_list=email_template_list)


@app.route('/send_email_indl_donor_compose', methods=['POST'])
def send_email_indl_donor_compose():
    template_name = request.form['template_name']
    donor_id = request.form['donor_id']
    donor_obj = sub_process.donor_details_byid(donor_id)
    donor_previous_phone_logs = sub_process.donor_phone_logs_byid(donor_id)
    donor_previous_email_logs = sub_process.donor_email_logs_byid(donor_id)
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    email_template_obj = sub_process.get_email_template_obj(template_name, donor_obj, session['logged_user_full_name'])

    return render_template('send_email_indl_donor_compose.html', donor_obj=donor_obj,
                           phone_log=donor_previous_phone_logs,
                           email_log=donor_previous_email_logs,
                           current_date=current_date, current_time=current_time, email_template_obj=email_template_obj)


@app.route('/send_email_indl_donor_transmit', methods=['POST'])
def send_email_indl_donor_transmit():
    donor_id = request.form['donor_id']
    contact_person = request.form['contact_person']
    contact_date = request.form['contact_date']
    contact_time = request.form['contact_time']
    salutation = request.form['salutation']
    main_body = request.form['main_body']
    closing = request.form['closing']
    signature = request.form['signature_block']
    sub_process.transmit_indl_email(donor_id=donor_id, contact_person=contact_person, contact_date=contact_date,
                                    contact_time=contact_time,
                                    salutation=salutation, main_body=main_body, closing=closing, signature=signature)
    return redirect(url_for('index'))


@app.route('/send_bulk_email_donor')
def send_bulk_email_donor():
    try:
        if session['login_status'] == 'True' and (
                            session['logged_user_type'] == 'Administrator' or session[
                        'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):

            donor_list = sub_process.get_donor_list()
            email_template_list=sub_process.get_email_template_list()
            return render_template('send_bulk_email_donor.html', donor_list=donor_list,email_template_list=email_template_list)

        else:
            return render_template('invalid_login.html')
    except:

        return render_template('invalid_login.html')


@app.route('/send_bulk_email_donor_process', methods=['POST'])
def send_bulk_email_donor_process():
    button_code=request.form['submit']
    sender = session['logged_username']
    sub_process.add_donor_bulk_email_list(donor_id=button_code, sender_username=sender)
    return redirect(url_for('send_bulk_email_donor'))

@app.route('/send_bulk_email_donor_compose', methods=['POST'])
def send_bulk_email_donor_compose():
    template_name = request.form['template_name']
    bulk_email_donor_details = sub_process.get_bulk_email_donor_details(session['logged_username']) 
    email_template_obj = sub_process.get_bulk_email_template_obj(template_name, session['logged_user_full_name'])
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    return render_template('send_bulk_email_donor_compose.html', donor_list=bulk_email_donor_details,email_template_obj=email_template_obj,current_date=current_date,current_time=current_time)

@app.route('/send_bulk_email_donor_transmit', methods=['POST'])
def send_bulk_email_donor_transmit():
    bulk_email_donor_details = sub_process.get_bulk_email_donor_details(session['logged_username'])
    contact_person = request.form['contact_person']
    contact_date = request.form['contact_date']
    contact_time = request.form['contact_time']
    salutation = request.form['salutation']
    main_body = request.form['main_body']
    closing = request.form['closing']
    signature = request.form['signature_block']
    sub_process.transmit_bulk_email(bulk_email_donor_details=bulk_email_donor_details,contact_person=contact_person, contact_date=contact_date,
                                    contact_time=contact_time,
                                    salutation=salutation, main_body=main_body, closing=closing, signature=signature, sender_username=session['logged_username'])
    return redirect(url_for('index'))

@app.route('/send_bulk_email_donor_merge')
def send_bulk_email_donor_merge():
    try:
        if session['login_status'] == 'True' and (
                            session['logged_user_type'] == 'Administrator' or session[
                        'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):

            donor_list = sub_process.get_donor_list()
            email_template_list=sub_process.get_email_template_list()
            return render_template('send_bulk_email_merge_donor.html', donor_list=donor_list,email_template_list=email_template_list)

        else:
            return render_template('invalid_login.html')
    except:

        return render_template('invalid_login.html')

@app.route('/send_bulk_email_donor_merge_process', methods=['POST'])
def send_bulk_email_donor_merge_process():
    button_code=request.form['submit']
    sender = session['logged_username']
    sub_process.add_donor_bulk_email_list(donor_id=button_code, sender_username=sender)
    return redirect(url_for('send_bulk_email_donor_merge'))

@app.route('/send_bulk_email_donor_merge_compose', methods=['POST'])
def send_bulk_email_donor_merge_composee():
    template_name = request.form['template_name']
    bulk_email_donor_details = sub_process.get_bulk_email_donor_details(session['logged_username'])
    email_template_obj = sub_process.get_bulk_email_template_obj(template_name, session['logged_user_full_name'])
    current_date = datetime.datetime.now().date().strftime("%m-%d-%Y")
    current_time = datetime.datetime.now().time().strftime("%H:%M")
    mail_merge_tag_file=config.MAIL_MERGE_TAG_FILE
    with open(mail_merge_tag_file) as merge_fh:
        merge_tags=json.load(merge_fh)
    return render_template('send_bulk_email_merge_donor_compose.html', donor_list=bulk_email_donor_details,email_template_obj=email_template_obj,current_date=current_date,current_time=current_time,merge_tags=merge_tags)

@app.route('/send_bulk_email_donor_merge_transmit', methods=['POST'])
def send_bulk_email_donor_merge_transmit():
    bulk_email_donor_details = sub_process.get_bulk_email_donor_details(session['logged_username'])
    contact_person = request.form['contact_person']
    contact_date = request.form['contact_date']
    contact_time = request.form['contact_time']
    salutation = request.form['salutation']
    main_body = request.form['main_body']
    closing = request.form['closing']
    signature = request.form['signature_block']
    sub_process.transmit_bulk_email_merge(bulk_email_donor_details=bulk_email_donor_details,contact_person=contact_person, contact_date=contact_date,
                                    contact_time=contact_time,
                                    salutation=salutation, main_body=main_body, closing=closing, signature=signature, sender_username=session['logged_username'])
    return redirect(url_for('index'))

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
    try:
        if session['login_status'] == 'True' and (
                            session['logged_user_type'] == 'Administrator' or session[
                        'logged_user_type'] == 'Supervisor' or session['logged_user_type'] == 'Volunteer'):
            donor_list = sub_process.alotted_donors_byid(session['logged_user_full_name'])
            if len(donor_list) > 0:
                return render_template('commit_donation.html', donor_list=donor_list)
            else:
                return render_template('commit_donation.html')

        else:
            return render_template('invalid_login.html')
    except:

        return render_template('invalid_login.html')


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
    form = DonationCommitForm(request.form)
    donor_id = request.form['donor_id']
    if not form.validate() or not sub_process.find_donor(donor_id):
        print(form.errors)
        return redirect(url_for('commit_donation'))
    commit_date = form.commit_date.data
    commit_date = commit_date.strftime("%Y-%m-%d")
    commit_time = form.commit_time.data
    commit_amt = form.committed_amt.data
    currency = form.currency.data
    payment_mode = form.payment_mode.data
    remarks = form.remarks.data
    sub_process.commit_donation(donor_id=donor_id, commit_date=commit_date, commit_time=commit_time,
                                commit_amt=commit_amt, currency=currency, payment_mode=payment_mode, remarks=remarks)
    return redirect(url_for('index'))


@app.route('/create_new_emailtemplate')
def create_new_emailtemplate():
    return render_template('create_new_emailtemplate.html')


@app.route('/new_emailtemplate_process', methods=['POST'])
def new_emailtemplate_process():
    template_name = request.form['template_name']
    salutation = request.form['salutation']
    main_body = request.form['main_body']
    closing = request.form['closing']
    signature_block = request.form['signature_block']
    sub_process.add_new_emailtemplate(template_name=template_name, salutation=salutation, main_body=main_body,
                                      closing=closing, signature_block=signature_block)
    return redirect(url_for('index'))
