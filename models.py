from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DOUBLE, DATE, TIME, LONGBLOB, ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from leaderboard import db

Base = declarative_base()


class User(db.Model):
    __tablename__ = 'workflow_users'

    username = db.Column(VARCHAR(50), primary_key=True)
    full_name = db.Column(VARCHAR(80), nullable=False)
    email = db.Column(VARCHAR(100), unique=True, nullable=False)
    phone = db.Column(DOUBLE)
    passwd = db.Column(VARCHAR(100), nullable=False)
    user_type = db.Column(db.Enum("Administrator", "Supervisor", "Volunteer"), nullable=False)
    register_date = db.Column(DATE, nullable=False)
    account_status = db.Column(db.Enum("Active", "Pending"), nullable=False)

    def __init__(self, username=None, full_name=None, email=None, phone=None, user_type=None,
                 register_date=None, account_status=None, passwd=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.user_type = user_type
        self.register_date = register_date
        self.account_status = account_status
        self.passwd = passwd

    def __repr__(self):
        return '<User %r>' % (self.username)


class Donor(db.Model):
    __tablename__ = 'donor_details'
    id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(VARCHAR(15))
    name = db.Column(VARCHAR(80), nullable=False)
    donor_status = db.Column(ENUM("New", "Allotted", "Committed", "Transferred"), nullable=False)
    phone = db.Column(VARCHAR(12))
    email = db.Column(VARCHAR(100), unique=True, nullable=False)
    org = db.Column(VARCHAR(200))
    contact_person = db.Column(VARCHAR(80), nullable=False)
    contact_date = db.Column(DATE, nullable=False)
    anonymous_select = db.Column(ENUM("Yes", "No"), default="No")
    volunteer_name = db.Column(VARCHAR(80), nullable=True)

    def __init__(self, title=None, name=None, email=None, phone=None, donor_status=None,
                 org=None, contact_person=None, contact_date=None, anonymous_select=None,
                 volunteer_name=None):
        self.title = title
        self.name = name
        self.email = email
        self.phone = phone
        self.donor_status = donor_status
        self.org = org
        self.contact_date = contact_date
        self.contact_person = contact_person
        self.anonymous_select = anonymous_select
        self.volunteer_name = volunteer_name

    def __repr__(self):
        return '<Donor%r>' % (self.name)


class DonorPhoneLog(db.Model):
    __tablename__ = 'donor_phone_logs'
    log_id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    contact_date = db.Column(DATE, nullable=False)
    contact_time = db.Column(TIME, nullable=False)
    contact_person = db.Column(VARCHAR(80), nullable=False)
    donor_id = db.Column(INTEGER, nullable=False)
    remarks = db.Column(LONGBLOB)
    details_shared = db.Column(LONGBLOB)

    def __init__(self, contact_date=None, contact_time=None,
                 contact_person=None, donor_id=None, remarks=None, details_shared=None):
        self.contact_date = contact_date
        self.contact_time = contact_time
        self.contact_person = contact_person
        self.donor_id = donor_id
        self.remarks = remarks
        self.details_shared = details_shared

    def __repr__(self):
        return '<LogID%r>' % (self.log_id)

class DonorEmailLog(db.Model):
    __tablename__ = 'donor_email_logs'
    log_id = db.Column(INTEGER, primary_key=True, autoincrement=True)
    contact_date = db.Column(DATE, nullable=False)
    contact_time = db.Column(TIME, nullable=False)
    contact_person = db.Column(VARCHAR(80), nullable=False)
    donor_id = db.Column(INTEGER, nullable=False)
    main_body=db.Column(LONGBLOB, nullable=False)
    full_email = db.Column(LONGBLOB)
    mail_code=db.Column(VARCHAR(20), nullable=False)

    def __init__(self, contact_date=None, contact_time=None,
                 contact_person=None, donor_id=None, main_body=None, full_email=None,mail_code=None):
        self.contact_date = contact_date
        self.contact_time = contact_time
        self.contact_person = contact_person
        self.donor_id = donor_id
        self.main_body = main_body
        self.full_email = full_email
        self.mail_code=mail_code

    def __repr__(self):
        return '<LogID%r>' % (self.log_id)


class CommittedDonation(db.Model):
    __tablename__ = 'committed_donation_details'
    donation_commit_id=db.Column(INTEGER, primary_key=True,nullable=False,autoincrement=True)
    donor_id=db.Column(INTEGER, nullable=False)
    commit_date = db.Column(DATE, nullable=False)
    commit_time = db.Column(TIME, nullable=False)
    commit_amt = db.Column(INTEGER, nullable=False)
    currency= db.Column(db.Enum('USD', 'GBP', 'EUR', 'BITCOIN'), nullable=False)
    payment_mode=db.Column(db.Enum('Paypal', 'Online Bank', 'CreditCard', 'Crypto', 'Cheque'), nullable=False)
    remarks = db.Column(LONGBLOB)


    def __init__(self,donor_id=donor_id,commit_date=commit_date,commit_time=commit_time,
                 commit_amt=commit_amt,currency=currency,payment_mode=payment_mode,remarks=remarks):
        self.donor_id = donor_id
        self.commit_date = commit_date
        self.commit_time = commit_time
        self.commit_amt=commit_amt
        self.currency=currency
        self.payment_mode=payment_mode
        self.remarks = remarks

    def __repr__(self):
        return '<DonationCommitID%r>' % (self.donation_commit_id)

class EmailTemplate(db.Model):
    __tablename__ = 'email_templates'
    template_id=db.Column(INTEGER, primary_key=True,nullable=False,autoincrement=True)
    template_name=db.Column(VARCHAR(50), nullable=False,unique=True)
    salutation=db.Column(VARCHAR(80), nullable=False)
    main_body=db.Column(db.Text, nullable=False)
    closing=db.Column(VARCHAR(100), nullable=False)
    signature_block=db.Column(VARCHAR(150), nullable=False)

    def __init__(self,template_name=template_name,salutation=salutation,main_body=main_body,
                 closing=closing,signature_block=signature_block):
        self.template_name = template_name
        self.salutation = salutation
        self.main_body = main_body
        self.closing=closing
        self.signature_block=signature_block

    def __repr__(self):
        return '<TemplateID%r>' % (self.template_id)

class BulkEmailList(db.Model):
    __tablename__ = 'bulk_email_list'
    mail_id=db.Column(INTEGER, primary_key=True,nullable=False,autoincrement=True)
    donor_id=db.Column(INTEGER, nullable=False)
    username = db.Column(VARCHAR(50),nullable=False)

    def __init__(self,donor_id=donor_id,username=username):
        self.donor_id = donor_id
        self.username= username

    def __repr__(self):
        return '<DonorID%r>' % (self.donor_id)