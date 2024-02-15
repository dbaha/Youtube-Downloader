from pytube import YouTube
import requests

# Replace 'YOUR_VIDEO_URL' with the actual YouTube video URL
video_url = 'https://music.youtube.com/watch?v=Q_2KGjfMBRs&list=RDAMVMQ_2KGjfMBRs'

# Create a YouTube object
yt = YouTube(video_url)

# Get the thumbnail URL
thumbnail_url = yt.thumbnail_url

# Download the thumbnail using requests
thumbnail_filename = 'thumbnail.jpg'  # You can change the filename if needed
response = requests.get(thumbnail_url)

with open(thumbnail_filename, 'wb') as file:
    file.write(response.content)

print(f'Thumbnail downloaded and saved as {thumbnail_filename}')
