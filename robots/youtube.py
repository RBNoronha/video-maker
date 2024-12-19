import os
import json
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from state import save, load

def authenticate_with_oauth():
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None
    if os.path.exists("token.json"):
        with open("token.json", "r") as token:
            creds = google.auth.load_credentials_from_file(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/google-youtube.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def upload_video(content):
    creds = authenticate_with_oauth()
    youtube = build("youtube", "v3", credentials=creds)
    video_file_path = "./content/video-maker.mp4"
    video_file_size = os.path.getsize(video_file_path)
    video_title = f"{content['prefix']} {content['searchTerm']}"
    video_tags = [content["searchTerm"]] + content["sentences"][0]["keywords"]
    video_description = "\n\n".join(
        [sentence["text"] for sentence in content["sentences"]]
    )

    request_body = {
        "snippet": {
            "title": video_title,
            "description": video_description,
            "tags": video_tags,
        },
        "status": {"privacyStatus": "unlisted"},
    }

    media_body = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media_body
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Video available at: https://youtu.be/{response['id']}")
    return response

def upload_thumbnail(video_information):
    creds = authenticate_with_oauth()
    youtube = build("youtube", "v3", credentials=creds)
    video_id = video_information["id"]
    video_thumbnail_file_path = "./content/youtube-thumbnail.jpg"

    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(video_thumbnail_file_path),
    )

    response = request.execute()
    print("Thumbnail uploaded!")

def run():
    content = load()
    video_information = upload_video(content)
    upload_thumbnail(video_information)
    save(content)

if __name__ == "__main__":
    run()
