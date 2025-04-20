import os
import csv
import json
from googleapiclient.discovery import build

# Configuration
API_KEY = os.getenv('YOUTUBE_API_KEY', 'your-api-key-here')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID', '@bustyle9734')  # Using channel handle

def get_channel_videos():
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    try:
        # First get channel details
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=CHANNEL_ID
        ).execute()
        
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get playlist items
        videos = []
        next_page_token = None
        
        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_response = youtube.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                
                video_data = video_response['items'][0]['snippet']
                videos.append({
                    'title': video_data['title'],
                    'youtube_url': f'https://youtu.be/{video_id}',
                    'description': video_data['description'],
                    'published_at': video_data['publishedAt'],
                    'thumbnail': video_data['thumbnails']['high']['url']
                })
            
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos
    
    except Exception as e:
        print(f'API Error: {str(e)}')
        return []

if __name__ == '__main__':
    video_data = get_channel_videos()
    
    # JSON output
    with open('channel_videos.json', 'w') as f:
        json.dump(video_data, f, indent=2)
    
    # CSV output matching Django model
    with open('channel_videos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'title', 
            'youtube_url', 
            'description',
            'published_at',
            'category'
        ])
        writer.writeheader()
        # Map category based on video content
        for video in video_data:
            video['category'] = '3D Printing' if '3D' in video['title'] else 'General'
        writer.writerows(video_data)