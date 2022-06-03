# -*- coding: utf-8 -*-
from apiclient.http import MediaFileUpload
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import pprint
import io
from datetime import date

scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('token.json', scopes)
http_auth = credentials.authorize(Http())
drive = build('drive', 'v3', http=http_auth)

def share_link(drive,file_id):
   share_link = drive.files().get(
   fileId = file_id,
   fields = 'webViewLink'
   ).execute()
   return share_link

def delete_files(drive,file_id):
   drive.files().delete(fileId=file_id).execute()

def create_folders(drive,name_folder):
   file_metadata = {
                'name': name_folder,
                'mimeType': 'application/vnd.google-apps.folder',
            }
   results = drive.files().create(body=file_metadata, fields='id').execute()
   return results['id']

def upload_files(drive,folder_id,name_file,file_path):
   file_metadata = {
                'name': name_file,
                'parents': [folder_id]
            }
   media = MediaFileUpload(file_path, resumable=True)
   results = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
   return results['id']

def files_list(drive):
   results = drive.files().list(pageSize=10,fields="nextPageToken, files(id, name, mimeType)").execute()
   return results['files']

def add_permissions(drive,file_id,email):
   user_permission = {
     'type' : 'user',
     'role' : 'writer',
     'emailAddress' : email
   }
   results = drive.permissions().create(
       fileId = file_id,
       body = user_permission,
       fields = 'id',
    ).execute()
