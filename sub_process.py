import config, os, pickle, datetime
from leaderboard import *
from models import User, Donor, DonorPhoneLog,CommittedDonation,EmailTemplate
from werkzeug.security import generate_password_hash, check_password_hash


# User Authentication Method Using MySQL Database.
# This method returns the login_status, user_account_type and user full name if the user is authenticated ,
# else it returns a None object
# Return function is views.user_login_process()
def authenticate(username, password):
    print 'Authentication Module'
    login_status = False
    user_account_type = None
    user_full_name = None
    query_result = User.query.filter_by(username=username).first()
    if query_result is not None:
        print query_result
        query_passwd = query_result.passwd
        passwd_check = check_password_hash(query_passwd, password)
        if passwd_check is True:
            login_status = True
            user_account_type = query_result.user_type
            user_full_name = str(query_result.full_name)
    return (login_status, user_account_type, user_full_name)


def write_user_log(str):
    userlogfile = config.USER_LOG_FILE
    userlogfh = open(userlogfile, 'a+')
    userlogfh.write(str)
    userlogfh.write('\n')
    userlogfh.close()


# This method returns the list of all existing donors in the donor_details table in the donorworkflow database
def get_donor_list():
    query_result = Donor.query.all()
    query_length = len(query_result)
    return query_result


# Retrieves Pending User list from the MySQL Database to be used to approve/reject new Users.
# Returning Function is views.approve_new_user()

def get_pending_user_list():
    query_result = User.query.filter_by(account_status='Pending').all()
    return query_result


# This method changes the user account_status
# to 'Approved' in the workflow_users table in the MySQL donorworkflow database
# once the Administrator has approved the User Account
def approve_user(username):
    user_details = User.query.filter_by(username=username).first()
    user_details.account_status = 'Active'
    db.session.commit()


# This method deletes the user details in the workflow_users table in thr donorworkflow Database
# once the Administrator has Rejected the User Account
def reject_user(username):
    user_details = User.query.filter_by(username=username).first()
    db.session.delete(user_details)
    db.session.commit()


# This method add the records of a new donor to the donor_details table of the
# donorworkflow database
def register_new_donor(title, name, org, email, donor_contact, contact_person,
                       contact_date, anonymous_select):
    if donor_contact == '':
        donor_contact = None
    db.session.add(Donor(title=title, name=name, email=email, phone=donor_contact,
                         donor_status='New', org=org, contact_person=contact_person,
                         contact_date=contact_date, anonymous_select=anonymous_select,
                         volunteer_name=None))
    db.session.commit()


# This method returns the details of a donor by searching the details of the user
# in the donor_details table of the donorworkflow database
def donor_details_byid(donor_id):
    donor_details = Donor.query.filter_by(id=donor_id).first()
    return donor_details

# This method return the phone conversation log with a Donor based on hid donor_id from the donor_contact_logs
# table in the donorworkflow database.
# The details are returned to views.donor_phone_contact_process()
# Disabled Currently due to migration to MySQL Database
def donor_phone_logs_byid(donor_id):
    phone_logs = DonorPhoneLog.query.filter_by(donor_id=donor_id).all()
    return phone_logs

# This method return the phone conversation log with a Donor based on his donor_id
# from the DONOR_CONTACT_LOGS pickle file.
# The details are returned to views.donor_phone_contact_process()
# Disabled Currently due to migration to MySQL Database
# def donor_phone_logs_byid(donor_id):
#     donor_contact_log_file = config.DONOR_CONTACT_LOGS_FILE
#     pickle_obj = None
#     contact_logs = []
#     if os.path.exists(donor_contact_log_file):
#         fh = open(donor_contact_log_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         for i in range(0, obj_len):
#             if int(pickle_obj[i]['donor_id']) == int(donor_id):
#                 contact_logs.append(pickle_obj[i])
#     return contact_logs


# This method updates the donor_phone_logs table in the donorworkflow database with the details of the latest
# telephonic conversation with the Donor
def add_donor_phone_log(donor_id, contact_person, contact_date, contact_time, details_shared,
                        remarks):
    db.session.add(DonorPhoneLog(contact_date=contact_date,contact_time=contact_time,
                                 contact_person=contact_person,donor_id=donor_id,remarks=remarks,
                                 details_shared=details_shared))
    db.session.commit()
    return None


# This method is called by views.donor_contact_update_form_process()
# for updating contact information of the donor with the specified ID
# in the donor_details table in the donorworkflow database
def update_donor_contact(donor_id, phone, email):
    user_details = Donor.query.filter_by(id=donor_id).first()
    user_details.phone = phone
    user_details.email = email
    db.session.commit()


def donor_email_logs_byid(donor_id):
    donor_email_log_file = config.DONOR_EMAIL_LOG_FILE
    pickle_obj = None
    email_logs = []
    if os.path.exists(donor_email_log_file):
        fh = open(donor_email_log_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if int(pickle_obj[i]['donor_id']) == int(donor_id):
                email_logs.append(pickle_obj[i])
    return email_logs


def get_new_donor_list():
    new_donor_list = Donor.query.filter_by(donor_status='New').all()
    return new_donor_list


def get_volunteer_list():
    volunteer_list = User.query.filter_by(user_type='Volunteer').filter_by(account_status='Active').all()
    print volunteer_list
    # user_account_file = config.USER_DETAILS_PICKLE_FILE
    #volunteer_list = []
    #if os.path.exists(user_account_file):
    #    fh = open(user_account_file, 'rb')
    #    pickle_obj = pickle.load(fh)
    #    obj_len = len(pickle_obj)
    #    for i in range(0, obj_len):
    #        if pickle_obj[i]['user_type'] == 'Volunteer' and pickle_obj[i]['account_status'] == 'Active':
    #            volunteer_list.append(pickle_obj[i])

    return volunteer_list


def allot_volunteer(donor_id, volunteer_name):
    donor = Donor.query.get(donor_id)
    donor.volunteer_name = volunteer_name
    donor.donor_status = 'Allotted'
    db.session.commit()
    # donor_file = config.DONOR_DETAILS_PICKLE_FILE
    # donor_list = []
    # if os.path.exists(donor_file):
    #     fh = open(donor_file, 'rb')
    #     pickle_obj = pickle.load(fh)
    #     obj_len = len(pickle_obj)
    #     for i in range(0, obj_len):
    #         if int(pickle_obj[i]['id']) != int(donor_id):
    #             donor_list.append(pickle_obj[i])
    #         else:
    #             pickle_obj[i]['volunteer_name'] = volunteer_name
    #             pickle_obj[i]['donor_status'] = 'Allotted'
    #             donor_list.append(pickle_obj[i])
    # with open(donor_file, 'wb') as wfp:
    #     pickle.dump(donor_list, wfp)


def alotted_donors_byid(username):
    allotted_donor_list = Donor.query.filter_by(volunteer_name=username).all()
    return allotted_donor_list
    # print username
    # donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    # alotted_donor_list = []
    # if os.path.exists(donor_details_file):
    #     fh = open(donor_details_file, 'rb')
    #     pickle_obj = pickle.load(fh)
    #     obj_len = len(pickle_obj)
    #     for i in range(0, obj_len):
    #         if 'volunteer_name' in pickle_obj[i]:
    #             if pickle_obj[i]['volunteer_name'] == username:
    #                 alotted_donor_list.append(pickle_obj[i])


def allotted_donors_byid(username):
    allotted_donor_list = Donor.query.filter_by(volunteer_name=username).all()
    return allotted_donor_list


# def commit_donation(donation_details):
#     print donation_details
#     donation_file = config.DONATION_AMT_FILE
#     donation_list = []
#     if os.path.exists(donation_file):
#         fh = open(donation_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         fh.close()
#         for i in range(0, obj_len):
#             donation_list.append(pickle_obj[i])
#     donation_list.append(donation_details)
#     with open(donation_file, 'wb') as wfp:
#         pickle.dump(donation_list, wfp)
#
#     donor_id = donation_details['donor_id']
#     print ('Donor ID:', donor_id)
#     donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
#     donor_details = []
#     if os.path.exists(donor_details_file):
#         fh = open(donor_details_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         fh.close()
#
#         for i in range(0, obj_len):
#
#             if int(pickle_obj[i]['id']) != int(donor_id):
#                 donor_details.append(pickle_obj[i])
#             else:
#                 print pickle_obj[i]
#                 pickle_obj[i]['donor_status'] = 'Committed'
#                 donor_details.append(pickle_obj[i])
#
#     print donor_details
#     with open(donor_details_file, 'wb') as wfp:
#         pickle.dump(donor_details, wfp)

def commit_donation(donor_id,commit_date,commit_time,commit_amt,currency,
                    payment_mode,remarks):
    print 'Currency:'+currency
    db.session.add(CommittedDonation(donor_id=donor_id,commit_date=commit_date,commit_time=commit_time,
                                     commit_amt=commit_amt,currency=currency,payment_mode=payment_mode,remarks=remarks))
    donor = Donor.query.get(donor_id)
    donor.donor_status = 'Committed'
    db.session.commit()

    return None

def add_user_details_db(name, email, user_contact, username, password, user_type):
    hashed_passwd = generate_password_hash(password)
    register_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
    account_status = 'Pending'
    db.session.add(User(username=username, full_name=name, email=email, phone=user_contact, user_type=user_type,
                        register_date=register_date, account_status=account_status, passwd=hashed_passwd))
    db.session.commit()
    return None

def add_new_emailtemplate(template_name,salutation,main_body,closing,
                          signature_block):
    db.session.add(EmailTemplate(template_name=template_name,salutation=salutation,main_body=main_body,
                                 closing=closing,signature_block=signature_block))
    db.session.commit()
    return None

def get_email_template_list():
    email_template_list = EmailTemplate.query.all()
    return email_template_list
