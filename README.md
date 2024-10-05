# MusicDownloader
Python script for downloading music from YouTube & Spotify. 

# Installation
Clone the repository:
```
git clone https://github.com/StudentPP1/YouTubeDownloader.git
```

Install the required packages:
```
pip install -r requirements.txt
```

run:
```
python main.py
```

# Usage
You can download the audio file from one video or download the whole playlist at once (if it is not private) 

The downloaded tracks will be saved in the 'Music' folder in the project

# Note
To use the script you need:
  * download [ffmpeg](https://ffmpeg.org/) and add the absolute path to 'ffmpeg.exe' to .env file
  * add CLIENT_ID and SECRET_ID from [Spotify](https://developer.spotify.com/documentation/web-api/concepts/apps) to .env file

