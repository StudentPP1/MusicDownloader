import os
import yt_dlp
import eyed3
import requests
import re
from pytube import Playlist
import shutil
from urllib import request as rq
from utils.const import ydl_opts, destination_path


class YouTube:
    def __init__(self):
        pass

    def _load_metadata_to_mp3(self, file_mp3, metadata):
        audiofile = eyed3.load(file_mp3)
        if audiofile.tag == None:
            audiofile.initTag()

        # Add basic tags
        title = metadata["track_name"]
        artist = metadata["artist_name"]
        track_name = f"{artist} - {title}"

        audiofile.tag.title = metadata["track_name"]
        audiofile.tag.album = metadata["album_name"]
        audiofile.tag.artist = metadata["artist_name"]
        audiofile.tag.release_date = metadata["album_date"]
        audiofile.tag.track_num = metadata["track_number"]

        album_art = rq.urlopen(metadata["album_art"]).read()
        audiofile.tag.images.set(3, album_art, "image/jpeg")
        audiofile.tag.save()

        os.rename(f"{file_mp3}", f"{track_name}.mp3")
        return f"{track_name}.mp3"

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
        audio = self._load_metadata_to_mp3(download_file, metadata)

        location = shutil.move(audio, f"{destination_path}\\{audio}")
        print(f"Done: {location}")

    def download_playlist(self, url):
        print("Getting playlist...")
        videos = Playlist(url)
        video_urls = [video_url for video_url in videos.video_urls]
        for video_url in video_urls:
            self.download_track(video_url)
            print(f"Done: {video_urls.index(video_url) + 1}/{len(video_urls)}")
