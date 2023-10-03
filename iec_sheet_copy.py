from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError
import os
import datetime


def copy_file(destination_folder_id):

    now = datetime.datetime.now()
    current_time_string = now.strftime("%Y%m%d%H%M%S%f")

    scope = ['https://www.googleapis.com/auth/drive'] 
    service_account_json_key = './iec-certificate-fe8128ae7e58.json'
    credentials = service_account.Credentials.from_service_account_file(
        filename = service_account_json_key,
        scopes=scope

    )

    service = build('drive', 'v3', credentials=credentials)

    newfile = {
                'name': current_time_string, 
                'parents' : [destination_folder_id]
              }
    originalId = '1p2G2br19t2AMUO4FHCLZVQN1L7KsFCtq9snoIpFbclE'
    service.files().copy(fileId=originalId, body=newfile).execute()
    print("I copied")
    return


