import config
import os
import pickle
import datetime
from leaderboard import *
from models import User, Donor, DonorPhoneLog, CommittedDonation, EmailTemplate, DonorEmailLog, BulkEmailList
from werkzeug.security import generate_password_hash, check_password_hash
import email_service
import json, re
from exception import EntityNotFoundError
from pprint import pprint


# User Authentication Method Using MySQL Database.
# This method returns the login_status, user_account_type and user full name if the user is authenticated ,
# else it returns a None object
# Return function is views.user_login_process()


def authenticate(username, password):
    login_status = False
    user_account_type = None
    user_full_name = None
    query_result = User.query.filter_by(username=username).first()
    if query_result is not None:
        query_passwd = query_result.passwd
        query_account_status = query_result.account_status
        passwd_check = check_password_hash(query_passwd, password)
        if passwd_check is True and query_account_status == 'Active':
            login_status = True
            user_account_type = query_result.user_type
            user_full_name = str(query_result.full_name)
    return (login_status, user_account_type, user_full_name)


# Authentication Method Using Pickle File
# This method returns the login_status, user_account_type and user full name if the user is authenticated ,
# else it returns a None object
# Return function is views.user_login_process()
# Disabled Currently due to migration to MySQL Database
# def authenticate(username, password):
#     login_status = False
#     user_account_type = None
#     user_full_name = None
#     user_pickle_file = config.USER_DETAILS_PICKLE_FILE
#     user_list = []
#     user_details_pickle_filename = config.USER_DETAILS_PICKLE_FILE
#
#     if os.path.exists(user_details_pickle_filename):
#         with open(user_details_pickle_filename, 'rb') as rfp:
#             user_list = pickle.load(rfp)
#             user_list_length = len(user_list)
#             for i in range(0, user_list_length):
#                 if user_list[i]['username'] == username:
#                     db_password = user_list[i]['password']
#                     db_account_type = user_list[i]['user_type']
#                     db_account_status = user_list[i]['account_status']
#                     db_user_fullname = user_list[i]['name']
#                     if password == db_password and db_account_status == 'Active':
#                         login_status = True
#                         user_account_type = db_account_type
#                         user_full_name = db_user_fullname
#                         return (login_status, user_account_type, user_full_name)
#
#     return (login_status, user_account_type, user_full_name)


def write_user_log(str):
    userlogfile = config.USER_LOG_FILE
    userlogfh = open(userlogfile, 'a+')
    userlogfh.write(str)
    userlogfh.write('\n')
    userlogfh.close()


# This method returns the list of all existing donors in the donor_details table in the donorworkflow database
def get_donor_list():
    query_result = Donor.query.all()
    return query_result


# This method returns the list of all existing donors in the DONOR_DETAILS pickle file
# Disabled Currently due to migration to MySQL Database
# def get_donor_list():
#     donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
#     pickle_obj = None
#     if os.path.exists(donor_details_file):
#         fh = open(donor_details_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         print(pickle_obj)
#     return pickle_obj


# Retrieves Pending User list from the MySQL Database to be used to approve/reject new Users.
# Returning Function is views.approve_new_user()

def get_pending_user_list():
    query_result = User.query.filter_by(account_status='Pending').all()
    return query_result


# Retrieves Pending User list from the Pickle to be used to approve/reject new Users.
# Returning Function is views.approve_new_user()
# Disabled Currently due to migration to MySQL Database
# def get_pending_user_list():
#     user_detail_file = config.USER_DETAILS_PICKLE_FILE
#     pending_user_list = []
#     if os.path.exists(user_detail_file):
#         fh = open(user_detail_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         for i in range(0, obj_len):
#             if pickle_obj[i]['account_status'] == 'Pending':
#                 pending_user_list.append(pickle_obj[i])
#
#     return pending_user_list

# This method changes the user account_status to 'Approved' in the USER_DETAILS_PICKLE file
# once the Administrator has approved the User Account
# Disabled Currently due to migration to MySQL Database
# def approve_user(username):
#     user_detail_file = config.USER_DETAILS_PICKLE_FILE
#     user_list = []
#     if os.path.exists(user_detail_file):
#         fh = open(user_detail_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         for i in range(0, obj_len):
#             if pickle_obj[i]['username'] != username:
#                 user_list.append(pickle_obj[i])
#             elif pickle_obj[i]['username'] == username:
#                 pickle_obj[i]['account_status'] = 'Active'
#                 user_list.append(pickle_obj[i])
#         fh.close()
#         with open(user_detail_file, 'wb') as wfp:
#             pickle.dump(user_list, wfp)


# This method changes the user account_status
# to 'Approved' in the workflow_users table in the MySQL donorworkflow database
# once the Administrator has approved the User Account
def approve_user(username):
    user_details = User.query.filter_by(username=username).first()
    if user_details is None:
        raise EntityNotFoundError
    user_details.account_status = 'Active'
    db.session.commit()


# This method deletes the user details in the USER_DETAILS_PICKLE file
# once the Administrator has Rejected the User Account
# Disabled Currently due to migration to MySQL Database
# def reject_user(username):
#     user_detail_file = config.USER_DETAILS_PICKLE_FILE
#     user_list = []
#     if os.path.exists(user_detail_file):
#         fh = open(user_detail_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         for i in range(0, obj_len):
#             if pickle_obj[i]['username'] != username:
#                 user_list.append(pickle_obj[i])
#             fh.close()
#         with open(user_detail_file, 'wb') as wfp:
#             pickle.dump(user_list, wfp)


# This method deletes the user details in the workflow_users table in thr donorworkflow Database
# once the Administrator has Rejected the User Account
def reject_user(username):
    user_details = User.query.filter_by(username=username).first()
    if user_details:
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


# This method add the records of a new donor to the DONOR DETAILS pickle file.
# This method is currently disabled due to migration to MySQL Database
# def register_new_donor(title, name, org, email, donor_contact, contact_person, contact_date,
#                            anonymous_select):
#     donor_list = []
#     donor_pickle_filename = config.DONOR_DETAILS_PICKLE_FILE
#     donor_list_len = 0
#     if os.path.exists(donor_pickle_filename):
#         with open(donor_pickle_filename, 'rb') as rfp:
#             donor_list = pickle.load(rfp)
#             donor_list_len = len(donor_list)
#     donor = {}
#     donor['id'] = donor_list_len + 1
#     donor['title'] = title
#     donor['name'] = name
#     donor['org'] = org
#     donor['phone'] = donor_contact
#     donor['email'] = email
#     donor['contact_person'] = contact_person
#     donor['contact_date'] = contact_date
#     donor['anonymous_select'] = anonymous_select
#     donor['donor_status'] = 'New'
#     donor_list.append(donor)
#     with open(donor_pickle_filename, 'wb') as wfp:
#         pickle.dump(donor_list, wfp)


# This method returns the details of a donor by searching the details of the user
# in the donor_details table of the donorworkflow database
def donor_details_byid(donor_id):
    donor_details = Donor.query.filter_by(id=donor_id).first()
    return donor_details


# This method returns the details of a donor by searching the details of the user
# in the DONOR_DETAILS pickel file
# Disabled Currently due to migration to MySQL Database
# def donor_details_byid(donor_id):
#     donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
#     pickle_obj = None
#     if os.path.exists(donor_details_file):
#         fh = open(donor_details_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         for i in range(0, obj_len):
#             if int(pickle_obj[i]['id']) == int(donor_id):
#                 return pickle_obj[i]
#

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
    db.session.add(DonorPhoneLog(contact_date=contact_date, contact_time=contact_time,
                                 contact_person=contact_person, donor_id=donor_id, remarks=remarks,
                                 details_shared=details_shared))
    db.session.commit()


# This method updates the DONOR_CONTACT_LOG pickle file with the details of the latest
# telephonic conversation with the Donor
# Disabled Currently due to migration to MySQL Database
# def add_donor_phone_log(donor_id, contact_person, contact_date, contact_time, details_shared,
#                         remarks):
#     donor_log = {}
#     donor_log['donor_id'] = donor_id
#     donor_log['contact_person'] = contact_person
#     donor_log['contact_date'] = contact_date
#     donor_log['contact_time'] = contact_time
#     donor_log['contact_mode'] = 'Phone'
#     donor_log['details_shared'] = details_shared
#     donor_log['remarks'] = remarks
#     donor_contact_log_file = config.DONOR_CONTACT_LOGS_FILE
#     pickle_obj = None
#     contact_logs = []
#     if os.path.exists(donor_contact_log_file):
#         fh = open(donor_contact_log_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         fh.close()
#         for i in range(0, obj_len):
#             contact_logs.append(pickle_obj[i])
#     contact_logs.append(donor_log)
#     with open(donor_contact_log_file, 'wb') as wfp:
#         pickle.dump(contact_logs, wfp)


# This method is called by views.donor_contact_update_form_process()
# for updating contact information of the donor with the specified ID
# in the donor_details table in the donorworkflow database
def update_donor_contact(donor_id, phone, email, org):
    user_details = Donor.query.filter_by(id=donor_id).first()
    if user_details is None:
        raise EntityNotFoundError
    user_details.phone = phone
    user_details.email = email
    user_details.org = org
    db.session.commit()


# This method is called by views.donor_contact_update_form_process()
# for updating contact information of the donor with the specified ID in the DONOR_DETAILS pickle file
# Disabled Currently due to migration to MySQL Database
# def update_donor_contact(donor_id, phone, email):
#     donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
#     donor_list = []
#     pickle_obj = None
#     if os.path.exists(donor_details_file):
#         fh = open(donor_details_file, 'rb')
#         pickle_obj = pickle.load(fh)
#         obj_len = len(pickle_obj)
#         for i in range(0, obj_len):
#             if int(pickle_obj[i]['id']) != int(donor_id):
#                 donor_list.append(pickle_obj[i])
#             else:
#                 pickle_obj[i]['phone'] = phone
#                 pickle_obj[i]['email'] = email
#                 donor_list.append(pickle_obj[i])
#     with open(donor_details_file, 'wb') as wfp:
#         pickle.dump(donor_list, wfp)


def donor_email_logs_byid(donor_id):
    # donor_email_log_file = config.DONOR_EMAIL_LOG_FILE
    # pickle_obj = None
    # email_logs = []
    # if os.path.exists(donor_email_log_file):
    #     fh = open(donor_email_log_file, 'rb')
    #     pickle_obj = pickle.load(fh)
    #     obj_len = len(pickle_obj)
    #     for i in range(0, obj_len):
    #         if int(pickle_obj[i]['donor_id']) == int(donor_id):
    #             email_logs.append(pickle_obj[i])
    # return email_logs
    email_logs = DonorEmailLog.query.filter_by(donor_id=donor_id).all()
    return email_logs


def get_new_donor_list():
    new_donor_list = Donor.query.filter_by(donor_status='New').all()

    # donor_detail_file = config.DONOR_DETAILS_PICKLE_FILE
    # new_donor_list = []
    # if os.path.exists(donor_detail_file):
    #     fh = open(donor_detail_file, 'rb')
    #     pickle_obj = pickle.load(fh)
    #     obj_len = len(pickle_obj)
    #     for i in range(0, obj_len):
    #         if pickle_obj[i]['donor_status'] == 'New':
    #             new_donor_list.append(pickle_obj[i])

    return new_donor_list


def get_volunteer_list():
    volunteer_list = User.query.filter_by(
        user_type='Volunteer').filter_by(account_status='Active').all()
    # user_account_file = config.USER_DETAILS_PICKLE_FILE
    # volunteer_list = []
    # if os.path.exists(user_account_file):
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
    if donor.donor_status == 'New':  # if a donor is already allotted or committed
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

    # return alotted_donor_list


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

def commit_donation(donor_id, commit_date, commit_time, commit_amt, currency,
                    payment_mode, remarks):
    db.session.add(CommittedDonation(donor_id=donor_id, commit_date=commit_date, commit_time=commit_time,
                                     commit_amt=commit_amt, currency=currency, payment_mode=payment_mode,
                                     remarks=remarks))
    donor = Donor.query.get(donor_id)
    donor.donor_status = 'Committed'
    db.session.commit()


def add_user_details_db(name, email, user_contact, username, password, user_type):
    hashed_passwd = generate_password_hash(password)
    register_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
    account_status = 'Pending'
    db.session.add(User(username=username, full_name=name, email=email, phone=user_contact, user_type=user_type,
                        register_date=register_date, account_status=account_status, passwd=hashed_passwd))
    db.session.commit()


def find_donor(donor_id):
    return Donor.query.get(donor_id)


def find_user_by_username(username):
    return User.query.get(username)


def find_user_by_email(email):
    return User.query.get(email)


def add_new_emailtemplate(template_name, salutation, main_body, closing,
                          signature_block):
    db.session.add(EmailTemplate(template_name=template_name, salutation=salutation, main_body=main_body,
                                 closing=closing, signature_block=signature_block))
    db.session.commit()


def get_email_template_list():
    email_template_list = EmailTemplate.query.all()
    return email_template_list


def get_email_template_obj(template_name, donor_obj, sender_name):
    if template_name != 'Manual Composition':
        template_obj = EmailTemplate.query.filter_by(
            template_name=template_name).all()
        template_package = template_obj[0]
        if donor_obj.title is not None:
            donor_full_name = donor_obj.title + ' ' + donor_obj.name
        else:
            donor_full_name = donor_obj.name
        template_package.salutation = template_package.salutation + ' ' + donor_full_name
        template_package.signature_block = sender_name + \
                                           '\n' + template_package.signature_block
    else:
        template_package = EmailTemplate()
        template_package.template_name = 'Manual Composition'
        template_package.salutation = ''
        template_package.main_body = ''
        template_package.closing = ''
        template_package.signature_block = ''

    return template_package


def get_bulk_email_template_obj(template_name, sender_name):
    if template_name != 'Manual Composition':
        template_obj = EmailTemplate.query.filter_by(
            template_name=template_name).all()
        template_package = template_obj[0]
        template_package.signature_block = sender_name + \
                                           '\n' + template_package.signature_block
    else:
        template_package = EmailTemplate()
        template_package.template_name = 'Manual Composition'
        template_package.salutation = ''
        template_package.main_body = ''
        template_package.closing = ''
        template_package.signature_block = ''

    return template_package


def transmit_indl_email(donor_id, contact_person, contact_date, contact_time, salutation,
                        main_body, closing, signature):
    donor = find_donor(donor_id)
    contact_date = datetime.datetime.strptime(contact_date, '%m-%d-%Y')
    contact_date = contact_date.date().strftime("%Y-%m-%d")
    message_obj, mail_code, msg_body = email_service.outgoing_mail_process(donor_email=donor.email,
                                                                           contact_person=contact_person,
                                                                           contact_date=contact_date,
                                                                           contact_time=contact_time,
                                                                           salutation=salutation, main_body=main_body,
                                                                           closing=closing, signature=signature)

    db.session.add(DonorEmailLog(contact_date=contact_date, contact_time=contact_time, contact_person=contact_person,
                                 donor_id=donor_id, main_body=main_body, full_email=msg_body, mail_code=mail_code))
    db.session.commit()


def add_donor_bulk_email_list(donor_id, sender_username):
    existing_list_check = BulkEmailList.query.filter_by(
        donor_id=donor_id).filter_by(username=sender_username).first()

    if existing_list_check is None:
        db.session.add(BulkEmailList(
            donor_id=donor_id, username=sender_username))
        db.session.commit()


def get_bulk_email_donor_details(sender_username):
    donor_list_query = BulkEmailList.query.filter_by(
        username=sender_username).all()
    donor_list = []
    for donors in donor_list_query:
        donor_list.append(int(donors.donor_id))
    donor_details = Donor.query.filter(Donor.id.in_(donor_list)).all()
    return donor_details


def transmit_bulk_email(bulk_email_donor_details, contact_person, contact_date, contact_time, salutation,
                        main_body, closing, signature, sender_username):
    contact_date = datetime.datetime.strptime(contact_date, '%m-%d-%Y')
    contact_date = contact_date.date().strftime("%Y-%m-%d")
    for donors in bulk_email_donor_details:
        if donors.title is not None:
            donor_full_name = donors.title + ' ' + donors.name
        else:
            donor_full_name = donors.name
        temp_salutation = salutation + ' ' + donor_full_name
        message_obj, mail_code, msg_body = email_service.outgoing_mail_process(donor_email=donors.email,
                                                                               contact_person=contact_person,
                                                                               contact_date=contact_date,
                                                                               contact_time=contact_time,
                                                                               salutation=temp_salutation,
                                                                               main_body=main_body,
                                                                               closing=closing, signature=signature)
        db.session.add(
            DonorEmailLog(contact_date=contact_date, contact_time=contact_time, contact_person=contact_person,
                          donor_id=donors.id, main_body=main_body, full_email=msg_body, mail_code=mail_code))
        db.session.commit()
        BulkEmailList.query.filter_by(username=sender_username).delete()


# def parse_for_merge_tags(string):
#     merge_tag_file=config.MAIL_MERGE_TAG_FILE
#     with open(merge_tag_file) as merge_fh:
#         merge_tags=json.load(merge_fh)
#         string_split=str(string).split()
#         for word in string_split:
#             if '$_' in word:
#                 for line in merge_tags:
#                     if word==line['tag']:
#                         print('Tag Found:',line['description'])
#                         model=line['model']
#                         query_field=line['map']
#                         print(model,query_field)
def replace_merge_tags(merge_tags, donor, searchtext):
    search_result = re.findall('([\$_]+[A-Z]+)', str(searchtext))
    return_text = str(searchtext)
    if len(search_result) > 0:
        for i in range(0, len(search_result)):
            tag = search_result[i]
            for line in merge_tags:
                if tag == line['tag']:
                    mapping = line['map']
                    for col in donor.__table__.columns:
                        col_name = str(col).split('.')[1]
                        if str(mapping) == str(col_name):
                            map_result = str(getattr(donor, str(mapping)))
                            return_text = return_text.replace(tag, map_result)
                            break
            return_text = return_text.replace(tag, '')

    return return_text


def transmit_bulk_email_merge(bulk_email_donor_details, contact_person, contact_date, contact_time, salutation,
                              main_body, closing, signature, sender_username):
    merge_tag_file = config.MAIL_MERGE_TAG_FILE
    merge_fh = open(merge_tag_file)
    merge_tags = json.load(merge_fh)
    contact_date = datetime.datetime.strptime(contact_date, '%m-%d-%Y')
    contact_date = contact_date.date().strftime("%Y-%m-%d")
    for donor in bulk_email_donor_details:

        contact_person_temp=contact_person
        salutation_temp=salutation
        main_body_temp=main_body
        closing_temp=closing
        signature_temp=signature
        contact_person_temp = replace_merge_tags(merge_tags=merge_tags, donor=donor, searchtext=contact_person_temp)
        salutation_temp = replace_merge_tags(merge_tags=merge_tags, donor=donor, searchtext=salutation_temp)
        main_body_temp = replace_merge_tags(merge_tags=merge_tags, donor=donor, searchtext=main_body_temp)
        closing_temp = replace_merge_tags(merge_tags=merge_tags, donor=donor, searchtext=closing_temp)
        signature_temp = replace_merge_tags(merge_tags=merge_tags, donor=donor, searchtext=signature_temp)
        message_obj, mail_code, msg_body = email_service.outgoing_mail_process(donor_email=donor.email,
                                                                               contact_person=contact_person_temp,
                                                                               contact_date=contact_date,
                                                                               contact_time=contact_time,
                                                                               salutation=salutation_temp,
                                                                               main_body=main_body_temp,
                                                                               closing=closing_temp, signature=signature_temp)
        db.session.add(
            DonorEmailLog(contact_date=contact_date, contact_time=contact_time, contact_person=contact_person_temp,
                          donor_id=donor.id, main_body=main_body_temp, full_email=msg_body, mail_code=mail_code))
        db.session.commit()
    BulkEmailList.query.filter_by(username=sender_username).delete()
    db.session.commit()