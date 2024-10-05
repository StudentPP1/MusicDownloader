import os
import yt_dlp
import eyed3
import requests
from pytube import Playlist
import shutil
import re
from urllib import request as rq
from utils.const import ydl_opts, destination_path


class YouTube:
    def __init__(self):
        pass

    def _load_metadata_to_mp3(self, file_mp3, metadata, url):
        audio_file = eyed3.load(file_mp3)
        if audio_file.tag == None:
            audio_file.initTag()

        video_id = url[url.index("=") + 1:]
        title = re.sub('[!@#$<>:\'\"\\/|*]', '', metadata["title"]) 
        with open("img.jpg", 'wb') as f:
            img = requests.get(f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg').content
            f.write(img)

        audio_file.tag.title = title.strip()
        audio_file.tag.images.set(3, open("img.jpg", 'rb').read(), 'image/jpeg')

        audio_file.tag.save()

        os.rename(f"{file_mp3}", f"{title}.mp3")
        return f"{title}.mp3"

    def download_track(self, url):
        print("Downloading track...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            metadata = ydl.extract_info(url, download=False)
            ydl.download([url])
  
        ready_to_convert = False
        download_file = None
        
        while not ready_to_convert:
            for file in os.listdir():
                if file.endswith(".mp3"):
                    ready_to_convert = True
                    download_file = file

        print("Loading metadata to audio...")
        audio = self._load_metadata_to_mp3(download_file, metadata, url)

        location = shutil.move(rf"{audio}", rf"{destination_path}\\{audio}")
        print(f"Done: {location}")

    def download_playlist(self, url):
        print("Getting playlist...")
        videos = Playlist(url)
        video_urls = [video_url for video_url in videos.video_urls]
        for video_url in video_urls:
            self.download_track(video_url)
            print(f"Done: {video_urls.index(video_url) + 1}/{len(video_urls)}")
