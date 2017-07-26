from wtforms import Form, StringField, validators, SelectField, DateField, IntegerField


class UserRegistrationForm(Form):
    user_full_name = StringField(u'Full Name', validators=[validators.required()])
    user_email = StringField(u'Email Address', validators=[validators.required(), validators.email()])
    user_contact = StringField(u'Contact Number', validators=[validators.optional()])
    username = StringField(u'Username', validators=[validators.required(), validators.Regexp(r'^\w+$')])
    user_password = StringField(u'Password', validators=[validators.required()])
    user_type = SelectField(u'User Type', choices=[
        ('Volunteer', 'Volunteer'),
        ('Supervisor', 'Supervisor'),
        ('Administrator', 'Administrator')])


class DonorAddForm(Form):
    donor_title = StringField(u'Donor Title', validators=[validators.required()])
    donor_name = StringField(u'Donor Name', validators=[validators.required()])
    donor_org = StringField(u'Donor Organization', validators=[validators.optional()])
    donor_email = StringField(u'Donor Email Address', validators=[validators.optional(), validators.email()])
    donor_contact = StringField(u'Donor Contact No.', validators=[validators.optional()])
    contact_person = StringField(u'Contact Person', validators=[validators.required()])
    contact_date = DateField(u'Contact Date', validators=[validators.required()], format='%m/%d/%Y')
    anonymous_select = SelectField(u'Anonymous', choices=[
        ('Yes', 'Yes'),
        ('No', 'No')
    ])


class DonorContactUpdateForm(Form):
    donor_contact = StringField(u'Donor Contact Number', validators=[validators.optional()])
    donor_email = StringField(u'Donor Email Address', validators=[validators.required(), validators.email()])
    donor_org=StringField(u'Donor Organisation', validators=[validators.optional()])

class DonationCommitForm(Form):
    commit_date = DateField(u'Commit Date', format='%m-%d-%Y', validators=[validators.required()])
    commit_time = StringField(u'Commit Time', validators=[validators.required()])
    committed_amt = IntegerField(u'Committed Amount', validators=[validators.required(), validators.NumberRange(min=1)])
    currency = SelectField(u'Currency', validators=[validators.required()], choices=[
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('BITCOIN', 'Bitcoin')
    ])
    payment_mode = SelectField(u'Payment Mode', validators=[validators.required()], choices=[
        ('Online Bank', 'Bank Transfer'),
        ('Paypal', 'Paypal'),
        ('Crypto', 'Crypto Currency'),
        ('CreditCard', 'Credit Card'),
        ('Cheque', 'Cheque')
    ])
    remarks = StringField(u'Remarks', validators=[validators.optional()])

