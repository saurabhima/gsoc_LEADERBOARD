from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, SET, DOUBLE, DATE, TIME, LONGBLOB
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
    user_type = db.Column(SET("Administrator", "Supervisor", "Volunteer"), nullable=False)
    register_date = db.Column(DATE, nullable=False)
    account_status = db.Column(SET("Active", "Pending"), nullable=False)

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
    donor_status = db.Column(SET("New", "Allotted", "Committed", "Transferred"), nullable=False)
    phone = db.Column(VARCHAR(12))
    email = db.Column(VARCHAR(100), unique=True, nullable=False)
    org = db.Column(VARCHAR(200))
    contact_person = db.Column(VARCHAR(80), nullable=False)
    contact_date = db.Column(DATE, nullable=False)
    anonymous_select = db.Column(SET("Yes", "No"), default="No")
    volunteer_name = db.Column(VARCHAR(80), nullable=True)

    def __init__(self, title=None, name=None, email=None, phone=None, donor_status=None,
                 org=None, contact_person=None, contact_date=None, anonymous_select=None,
                 voluneer_name=None):
        self.title = title
        self.name = name
        self.email = email
        self.phone = phone
        self.donor_status = donor_status
        self.org = org
        self.contact_date = contact_date
        self.contact_person = contact_person
        self.anonymous_select = anonymous_select
        self.volunteer_name = voluneer_name

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

    def __init__(self,contact_date=None, contact_time=None,
                 contact_person=None, donor_id=None, remarks=None, details_shared=None):

        self.contact_date = contact_date
        self.contact_time = contact_time
        self.contact_person = contact_person
        self.donor_id = donor_id
        self.remarks = remarks
        self.details_shared = details_shared

    def __repr__(self):
        return '<LogID%r>' % (self.log_id)
