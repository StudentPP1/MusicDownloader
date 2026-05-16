import os
import dotenv

dotenv.load_dotenv()

ydl_opts = {
    "cookiefile": "cookies.txt",
    "format": "bestaudio/best",
    "ignoreerrors": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
    "ffmpeg_location": os.getenv("FFMPEG_LOCATION"),
}

destination_path = "Music"
