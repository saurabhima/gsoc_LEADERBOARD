import config, os, pickle


def authenticate(username, password):
    login_status = False
    user_account_type = None
    user_full_name = None
    user_pickle_file = config.USER_DETAILS_PICKLE_FILE
    user_list = []
    user_details_pickle_filename = config.USER_DETAILS_PICKLE_FILE

    if os.path.exists(user_details_pickle_filename):
        with open(user_details_pickle_filename, 'rb') as rfp:
            user_list = pickle.load(rfp)
            user_list_length = len(user_list)
            for i in range(0, user_list_length):
                if user_list[i]['username'] == username:
                    db_password = user_list[i]['password']
                    db_account_type = user_list[i]['user_type']
                    db_account_status = user_list[i]['account_status']
                    db_user_fullname = user_list[i]['name']
                    if password == db_password and db_account_status == 'Active':
                        login_status = True
                        user_account_type = db_account_type
                        user_full_name = db_user_fullname
                        return (login_status, user_account_type, user_full_name)

    return (login_status, user_account_type, user_full_name)


def write_user_log(str):
    userlogfile = config.USER_LOG_FILE
    userlogfh = open(userlogfile, 'a+')
    userlogfh.write(str)
    userlogfh.write('\n')
    userlogfh.close()


def get_donor_list():
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    pickle_obj = None
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        print(pickle_obj)
    return pickle_obj


def get_pending_user_list():
    user_detail_file = config.USER_DETAILS_PICKLE_FILE
    pending_user_list = []
    if os.path.exists(user_detail_file):
        fh = open(user_detail_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if pickle_obj[i]['account_status'] == 'Pending':
                pending_user_list.append(pickle_obj[i])

    return pending_user_list


def approve_user(username):
    user_detail_file = config.USER_DETAILS_PICKLE_FILE
    user_list = []
    if os.path.exists(user_detail_file):
        fh = open(user_detail_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if pickle_obj[i]['username'] != username:
                user_list.append(pickle_obj[i])
            elif pickle_obj[i]['username'] == username:
                pickle_obj[i]['account_status'] = 'Active'
                user_list.append(pickle_obj[i])
        fh.close()
        with open(user_detail_file, 'wb') as wfp:
            pickle.dump(user_list, wfp)


def reject_user(username):
    user_detail_file = config.USER_DETAILS_PICKLE_FILE
    user_list = []
    if os.path.exists(user_detail_file):
        fh = open(user_detail_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if pickle_obj[i]['username'] != username:
                user_list.append(pickle_obj[i])
            fh.close()
        with open(user_detail_file, 'wb') as wfp:
            pickle.dump(user_list, wfp)


def donor_details_byid(donor_id):
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    pickle_obj = None
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if int(pickle_obj[i]['id']) == int(donor_id):
                return pickle_obj[i]
    return None


def donor_contact_logs_byid(donor_id):
    donor_contact_log_file = config.DONOR_CONTACT_LOGS_FILE
    pickle_obj = None
    contact_logs = []
    if os.path.exists(donor_contact_log_file):
        fh = open(donor_contact_log_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if int(pickle_obj[i]['donor_id']) == int(donor_id):
                contact_logs.append(pickle_obj[i])
    return contact_logs


def add_donor_log(donor_log):
    donor_contact_log_file = config.DONOR_CONTACT_LOGS_FILE
    pickle_obj = None
    contact_logs = []
    if os.path.exists(donor_contact_log_file):
        fh = open(donor_contact_log_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        fh.close()
        for i in range(0, obj_len):
            contact_logs.append(pickle_obj[i])
    contact_logs.append(donor_log)
    with open(donor_contact_log_file, 'wb') as wfp:
        pickle.dump(contact_logs, wfp)


def update_donor_contact(donor_id, phone, email):
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    donor_list = []
    pickle_obj = None
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if int(pickle_obj[i]['id']) != int(donor_id):
                donor_list.append(pickle_obj[i])
            else:
                pickle_obj[i]['phone'] = phone
                pickle_obj[i]['email'] = email
                donor_list.append(pickle_obj[i])
    with open(donor_details_file, 'wb') as wfp:
        pickle.dump(donor_list, wfp)


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
    donor_detail_file = config.DONOR_DETAILS_PICKLE_FILE
    new_donor_list = []
    if os.path.exists(donor_detail_file):
        fh = open(donor_detail_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if pickle_obj[i]['donor_status'] == 'New':
                new_donor_list.append(pickle_obj[i])

    return new_donor_list


def get_volunteer_list():
    user_account_file = config.USER_DETAILS_PICKLE_FILE
    volunteer_list = []
    if os.path.exists(user_account_file):
        fh = open(user_account_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if pickle_obj[i]['user_type'] == 'Volunteer' and pickle_obj[i]['account_status'] == 'Active':
                volunteer_list.append(pickle_obj[i])

    return volunteer_list


def allot_volunteer(donor_id, volunteer_name):
    donor_file = config.DONOR_DETAILS_PICKLE_FILE
    donor_list = []
    if os.path.exists(donor_file):
        fh = open(donor_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if int(pickle_obj[i]['id']) != int(donor_id):
                donor_list.append(pickle_obj[i])
            else:
                pickle_obj[i]['volunteer_name'] = volunteer_name
                pickle_obj[i]['donor_status'] = 'Allotted'
                donor_list.append(pickle_obj[i])
    with open(donor_file, 'wb') as wfp:
        pickle.dump(donor_list, wfp)


def alotted_donors_byid(username):
    print username
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    alotted_donor_list = []
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        for i in range(0, obj_len):
            if 'volunteer_name' in pickle_obj[i]:
                if pickle_obj[i]['volunteer_name'] == username:
                    alotted_donor_list.append(pickle_obj[i])

    return alotted_donor_list


def commit_donation(donation_details):
    print donation_details
    donation_file = config.DONATION_AMT_FILE
    donation_list = []
    if os.path.exists(donation_file):
        fh = open(donation_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        fh.close()
        for i in range(0, obj_len):
            donation_list.append(pickle_obj[i])
    donation_list.append(donation_details)
    with open(donation_file, 'wb') as wfp:
        pickle.dump(donation_list, wfp)

    donor_id = donation_details['donor_id']
    print ('Donor ID:',donor_id)
    donor_details_file = config.DONOR_DETAILS_PICKLE_FILE
    donor_details = []
    if os.path.exists(donor_details_file):
        fh = open(donor_details_file, 'rb')
        pickle_obj = pickle.load(fh)
        obj_len = len(pickle_obj)
        fh.close()

        for i in range(0, obj_len):

            if int(pickle_obj[i]['id']) != int(donor_id):
                donor_details.append(pickle_obj[i])
            else:
                print pickle_obj[i]
                pickle_obj[i]['donor_status'] = 'Committed'
                donor_details.append(pickle_obj[i])

    print donor_details
    with open(donor_details_file, 'wb') as wfp:
        pickle.dump(donor_details, wfp)
