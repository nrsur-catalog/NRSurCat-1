"""Module to help upload videos to youtube.

Requirements:
-------------

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


1. video-info.json: 
  Contains the path to the video, description, title. Also has two additional fields, uploaded (True if already uploaded, Flase by default) and the youtube_id (empty by default, filled in by this script).
2. Youtube API credentials:
  https://developers.google.com/youtube/v3/guides/uploading_a_video
  
"""

import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Set your OAuth 2.0 credentials
CLIENT_ID = os.environ.get('YOUTUBE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('YOUTUBE_CLIENT_SECRET')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
TOKEN_FILE = 'token.json'
VIDEO_INFO_FILE = 'video_info.json'

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def create_youtube_service(creds):
    return build('youtube', 'v3', credentials=creds)

def load_video_info():
    if os.path.exists(VIDEO_INFO_FILE):
        with open(VIDEO_INFO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_video_info(video_info):
    with open(VIDEO_INFO_FILE, 'w') as file:
        json.dump(video_info, file, indent=4)

def upload_video(youtube, video_path, title, description):
    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description,
            },
            'status': {
                'privacyStatus': 'public'
            }
        },
        media_body=MediaFileUpload(video_path)
    )
    response = request.execute()
    return response['id']

def main():
    creds = authenticate()
    youtube = create_youtube_service(creds)
    video_info = load_video_info()

    for video in video_info:
        if not video['uploaded']:
            video_id = upload_video(youtube, video['path'], video['title'], video['description'])
            video['youtube_id'] = video_id
            video['uploaded'] = True

    save_video_info(video_info)

if __name__ == "__main__":
    main()
