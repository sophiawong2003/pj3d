import requests
from bs4 import BeautifulSoup
import csv
import json

url = 'https://www.youtube.com/@bustyle9734/videos'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
videos = []

# Find all video elements (adjust selectors as needed)
for video in soup.find_all('a', href=True):
    if '/watch' in video['href']:
        video_url = f"https://www.youtube.com{video['href']}"
        title = video.get('title', 'No Title')
        description = video.get('aria-label', 'No Description')  # Adjust based on page structure

        videos.append({
            'url': video_url,
            'title': title,
            'description': description
        })

# Output as JSON
with open('videos.json', 'w') as json_file:
    json.dump(videos, json_file, indent=4)

# Output as CSV
with open('videos.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['url', 'title', 'description'])
    writer.writeheader()
    writer.writerows(videos)