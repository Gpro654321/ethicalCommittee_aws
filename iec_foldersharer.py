
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError


def share_folder(folder_to_share_id, user_email_id):
    '''
    folder_to_share_id = the id of the folder to share
    user_email_id = the user to whom the folder is to be shared
    
    the user is given only read access
    '''
    scope = ['https://www.googleapis.com/auth/drive'] 
    service_account_json_key = './iec-certificate-fe8128ae7e58.json'
    credentials = service_account.Credentials.from_service_account_file(
        filename = service_account_json_key,
        scopes=scope

    )

    service = build('drive', 'v3', credentials=credentials)

    user_permission = {
        'type' : 'user',
        'role' : 'reader',
        'emailAddress' : 'xxxxxxxxxxxxxx@gmail.com'
    }
    service.permissions().create(fileId='1XPYWkcCXvmBuJM8msWdV22HWmDqU-uci',
                                 body=user_permission,
                                 fields='id'
                                ).execute()

    print("I shared")
    return

