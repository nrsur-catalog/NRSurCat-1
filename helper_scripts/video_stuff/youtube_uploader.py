"""Module to help upload videos to youtube.

Requirements:
-------------

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


1. video-info.json: 
  Contains the path to the video, description, title. Also has two additional fields, uploaded (True if already uploaded, Flase by default) and the youtube_id (empty by default, filled in by this script).
2. Youtube API credentials:
  https://developers.google.com/youtube/v3/guides/uploading_a_video
  
"""

from tqdm.auto import tqdm
import os
import json
from upload_video import uploader, get_authenticated_service
from argparse import Namespace

VIDEO_INFO_FILE = 'video_info.json'


def load_video_info():
    if os.path.exists(VIDEO_INFO_FILE):
        with open(VIDEO_INFO_FILE, 'r') as file:
            return json.load(file)
    return []


def save_video_info(video_info):
    with open(VIDEO_INFO_FILE, 'w') as file:
        json.dump(video_info, file, indent=4)


def call_uploader(youtube, video_data):
    try:
        args = Namespace(
            file=video_data['path'],
            title=video_data['title'],
            description=video_data['description'],
            category="22",
            privacyStatus="unlisted",
            keywords="Gravitational Waves, Parameter Estimation, NRSurrogate"
        )
        return uploader(args, youtube)
    except Exception as e:
        print(f"Error uploading {video_data['path']}: {e}")
        return None


def main():
    youtube = get_authenticated_service()
    video_info = load_video_info()
    for video in tqdm(video_info, desc="Uploading videos"):
        if not video['uploaded']:
            video_id = call_uploader(youtube, video)
            video['youtube_id'] = video_id
            if video_id:
                video['uploaded'] = True

    save_video_info(video_info)


if __name__ == "__main__":
    main()
