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
