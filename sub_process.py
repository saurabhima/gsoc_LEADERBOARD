import config
import os
import pickle
import datetime
from leaderboard import *
from models import User, Donor, DonorPhoneLog, CommittedDonation, EmailTemplate, DonorEmailLog, BulkEmailList,CreditDonation
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


#
# Retrieves Pending User list from the MySQL Database to be used to approve/reject new Users.
# Returning Function is views.approve_new_user()
def get_pending_user_list():
    query_result = User.query.filter_by(account_status='Pending').all()
    return query_result


def approve_user(username):
    user_details = User.query.filter_by(username=username).first()
    if user_details is None:
        raise EntityNotFoundError
    user_details.account_status = 'Active'
    db.session.commit()


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



# This method updates the donor_phone_logs table in the donorworkflow database with the details of the latest
# telephonic conversation with the Donor
def add_donor_phone_log(donor_id, contact_person, contact_date, contact_time, details_shared,
                        remarks):
    donor = Donor.query.get(donor_id)
    if donor is None:
        raise EntityNotFoundError
    db.session.add(DonorPhoneLog(contact_date=contact_date, contact_time=contact_time,
                                 contact_person=contact_person, donor_id=donor_id, remarks=remarks,
                                 details_shared=details_shared))
    db.session.commit()


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

def donor_email_logs_byid(donor_id):
    email_logs = DonorEmailLog.query.filter_by(donor_id=donor_id).all()
    return email_logs


def get_new_donor_list():
    new_donor_list = Donor.query.filter_by(donor_status='New').all()
    return new_donor_list


def get_volunteer_list():
    volunteer_list = User.query.filter_by(
        user_type='Volunteer').filter_by(account_status='Active').all()
    return volunteer_list


def allot_volunteer(donor_id, volunteer_name):
    donor = Donor.query.get(donor_id)
    donor.volunteer_name = volunteer_name
    if donor.donor_status == 'New':  # if a donor is already allotted or committed
        donor.donor_status = 'Allotted'
    db.session.commit()


def alotted_donors_byid(username):
    allotted_donor_list = Donor.query.filter_by(volunteer_name=username).all()
    return allotted_donor_list

def committed_donors_byid():
    committed_donor_list=Donor.query.filter_by(donor_status='Committed').all()
    return committed_donor_list


def commit_donation(donor_id, commit_date, commit_time, commit_amt, currency,
                    payment_mode, remarks):
    db.session.add(CommittedDonation(donor_id=donor_id, commit_date=commit_date, commit_time=commit_time,
                                     commit_amt=commit_amt, currency=currency, payment_mode=payment_mode,
                                     remarks=remarks))
    donor = Donor.query.get(donor_id)
    donor.donor_status = 'Committed'
    db.session.commit()
def donor_commit_details_byid(donor_id):
    commitment_details=CommittedDonation.query.filter_by(donor_id=donor_id).first()
    return commitment_details

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
        template_package = EmailTemplate.query.filter_by(
            template_name=template_name).first()
        if template_package is None:
            raise EntityNotFoundError
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
        template_package = EmailTemplate.query.filter_by(
            template_name=template_name).first()
        if template_package is None:
            raise EntityNotFoundError
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

def credit_donation(donor_id, credit_date,credit_time,credited_amt,currency, payment_mode,credit_reference,payment_date,receipt_dispatch_mode, remarks):
    donor_details=donor_details_byid(donor_id)
    db.session.add(CreditDonation(donor_id=donor_id, credit_date=credit_date,credit_time=credit_time,amount=credited_amt,currency=currency, payment_mode=payment_mode,credit_reference=credit_reference,payment_date=payment_date,receipt_disp_mode=receipt_dispatch_mode, remarks=remarks))
    db.session.commit()
    print 'Generate Reciept Still Pending!'