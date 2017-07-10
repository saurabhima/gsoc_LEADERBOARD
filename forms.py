from wtforms import Form, StringField, validators, SelectField, DateField


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
    donor_org = StringField(u'Donor Organization', validators=[validators.required()])
    donor_email = StringField(u'Donor Email Address', validators=[validators.required(), validators.email()])
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