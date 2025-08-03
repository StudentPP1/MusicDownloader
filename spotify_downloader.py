import os
import shutil
import requests
import eyed3
import yt_dlp
from urllib import request as rq
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch
from const import ydl_opts, destination_path
import traceback

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = ["user-library-read"]


class Spotify:
    def __init__(self, token):
        self.spotify_base_url = "https://api.spotify.com/v1"
        self.headers = {"Authorization": f"Bearer {token}"}

    def _get_liked_tracks(self, limit=20):
        url = f"{self.spotify_base_url}/me/tracks?limit={limit}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return [item["track"]["id"] for item in data["items"]]

    def _get_track_data(self, track_id):
        url = f"{self.spotify_base_url}/tracks/{track_id}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        album_name = data["album"]["name"]
        album_release_date = data["album"]["release_date"]
        artist_names = [artist["name"] for artist in data["artists"]]
        duration_ms = data["duration_ms"]
        track_name = data["name"]
        images = [img["url"] for img in data["album"]["images"] if img["width"] == 300]
        return {
            "album_name": album_name,
            "album_release_date": album_release_date,
            "artist_names": artist_names,
            "duration_ms": f"{duration_ms // 1000 // 60}:{duration_ms % 1000}",
            "track_id": track_id,
            "track_name": track_name,
            "images": images,
        }

    def _download_track(self, track_data):
        search_term = (
            f"{track_data['track_name']} - {' '.join(track_data['artist_names'])}"
        )
        for ch in "()'\"&":
            search_term = search_term.replace(ch, "")
        print(f"Searching: {search_term}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                videosSearch = VideosSearch(search_term + " (Lyric video)", limit=5)
                result = videosSearch.result()["result"][0]
                if track_data["track_name"].lower() in result["title"].lower():
                    ydl.download(result["link"])
                else:
                    videosSearch = VideosSearch(search_term, limit=5)
                    result = videosSearch.result()["result"][0]
                    ydl.download(result["link"])
        except Exception as e:
            print("Download error:")
            traceback.print_exc()

    def _add_track_metadata(self, metadata, file_mp3):
        audiofile = eyed3.load(file_mp3)
        if audiofile.tag is None:
            audiofile.initTag()
        audiofile.tag.album = metadata["album_name"]
        audiofile.tag.release_date = metadata["album_release_date"]
        audiofile.tag.artist = metadata["artist_names"][0]
        audiofile.tag.title = metadata["track_name"]
        album_art = rq.urlopen(metadata["images"][0]).read()
        audiofile.tag.images.set(3, album_art, "image/jpeg")
        audiofile.tag.save()
        track_name = f"{metadata['artist_names'][0]} - {metadata['track_name']}.mp3"
        os.rename(file_mp3, track_name)
        location = shutil.move(track_name, os.path.join(destination_path, track_name))
        print(f"Saved to: {location}")

    def download_liked_tracks(self):
        track_ids = self._get_liked_tracks()
        for track_id in track_ids:
            track_data = self._get_track_data(track_id)
            self._download_track(track_data)

            ready_to_convert = False
            download_file = None
            while not ready_to_convert:
                for file in os.listdir():
                    if file.endswith(".mp3"):
                        ready_to_convert = True
                        download_file = file

            self._add_track_metadata(track_data, download_file)
