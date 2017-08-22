from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import config


def upload_receipt_gdrive(filename):
    gauth = GoogleAuth()
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'googledrive.json')
    gauth.LoadCredentialsFile(credential_path)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        gauth.SaveCredentialsFile(credential_path)

    drive = GoogleDrive(gauth)
    parentID = config.GDRIVE_PARENT_FOLDERID
    filepath=config.RECEIPT_DIRECTORY+'/'+filename
    f = drive.CreateFile({'title': filename, "parents": [{"kind": "drive#fileLink", "id": parentID}]})
    f.SetContentFile(filepath)
    f.Upload()
    permission = f.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'})
    # print(f['alternateLink'])
    # print(str(f))
    # print('title: %s, mimeType: %s' % (f['title'], f['mimeType']))
    return (f['alternateLink'])