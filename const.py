import os
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyClientCredentials

load_dotenv()

ydl_opts = {
    "format": "bestaudio/best",
    "ignoreerrors": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
    "ffmpeg_location": os.getenv("FFMPEG_LOCATION")}

destination_path = "Music"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("SECRET_ID")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("SECRET_ID")
))
