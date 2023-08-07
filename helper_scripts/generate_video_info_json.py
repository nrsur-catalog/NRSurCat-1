"""Generate the video-info.json needed for the youtube-uploader"""
import os
import sys
import glob
import json

VIDEO_INFO_FILE = 'video_info.json'

def generate_video_info(video_folder):
    video_info = []

    video_files = glob.glob(os.path.join(video_folder, '*.mp4'))  # Adjust the file extension if needed
    for video_file in video_files:
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        title = video_name
        description = f"This is a video named {video_name}."

        video_entry = {
            'path': video_file,
            'title': title,
            'description': description,
            'uploaded': False,
            'youtube_id': ''
        }
        video_info.append(video_entry)

    return video_info

def save_video_info(video_info):
    with open(VIDEO_INFO_FILE, 'w') as file:
        json.dump(video_info, file, indent=4)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_video_info_json.py <video_folder>")
        return

    video_folder = sys.argv[1]
    video_info = generate_video_info(video_folder)
    save_video_info(video_info)

if __name__ == "__main__":
    main()
