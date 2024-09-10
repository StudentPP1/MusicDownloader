import os
import shutil
from urllib import request as rq
import eyed3
import requests
import yt_dlp
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from youtubesearchpython import VideosSearch
from utils.const import ydl_opts, destination_path, client_id, client_secret


class Spotify:
    def __init__(self):
        self.spotify_base_url = "https://api.spotify.com/v1"
        token_url = 'https://accounts.spotify.com/api/token'

        oauth = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
        token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)

        access_token = token['access_token']

        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    def _get_playlist(self, playlist_id: str):
        url = f"{self.spotify_base_url}/playlists/{playlist_id}"
        resp = requests.get(url, headers=self.headers)
        data = resp.json()
        return data

    def _download_track(self, track_data):
        search_term = track_data['track_name'] + ' - ' + ' '.join(track_data['artist_names'])
        search_term = search_term.replace("(", "\(")
        search_term = search_term.replace(")", "\)")
        search_term = search_term.replace("'", r"\'")
        search_term = search_term.replace("\"", r'\"')
        search_term = search_term.replace("&", "\&")

        print(search_term + " (Lyric video)")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            videosSearch = VideosSearch(search_term + " (Lyric video)", limit=5)
            result = videosSearch.result()["result"][0]
            # print(result["link"], result["duration"], result["title"])
            ydl.download(result["link"])

    def _get_track_data(self, track_id):
        url = f"{self.spotify_base_url}/tracks/{track_id}"

        response = requests.get(url, headers=self.headers)

        data = response.json()
        album_type = data['album']['album_type']
        album_name = data['album']['name']
        album_release_date = data['album']['release_date']
        artist_names = [artist['name'] for artist in data['artists']]
        duration_ms = data['duration_ms']
        track_id = data['id']
        track_name = data['name']
        images = [image['url'] for image in data['album']['images'] if image['width'] == 300]

        return {
            'album_name': album_name,
            'album_release_date': album_release_date,
            'artist_names': artist_names,
            'duration_ms': f"{ duration_ms // 1000 // 60 }:{ duration_ms  % 1000 }",
            'track_id': track_id,
            'track_name': track_name,
            'images': images
        }

    def _add_track_metadata(self, metadata, file_mp3):
        audiofile = eyed3.load(file_mp3)
        if audiofile.tag == None:
            audiofile.initTag()

        # Add basic tags
        title = metadata["track_name"]
        artist = metadata["artist_names"][0]
        track_name = f"{artist} - {title}"

        audiofile.tag.album = metadata["album_name"]
        audiofile.tag.release_date = metadata["album_release_date"]
        audiofile.tag.artist = artist
        audiofile.tag.title = title

        album_art = rq.urlopen(metadata["images"][0]).read()
        audiofile.tag.images.set(3, album_art, "image/jpeg")
        audiofile.tag.save()

        os.rename(f"{file_mp3}", f"{track_name}.mp3")
        location = shutil.move(f"{track_name}.mp3", f"{destination_path}\\{track_name}.mp3")
        print(f"Done: {location}")

    def download_playlist(self, url):
        playlist_id = url.split('?')[0].split('/')[-1]
        data = self._get_playlist(playlist_id)
        items = data['tracks']['items']

        for item in items:
            track = item['track']
            track_data = self._get_track_data(track['id'])
            self._download_track(track_data)

            ready_to_convert = False
            download_file = None

            while not ready_to_convert:
                for file in os.listdir():
                    if file.endswith(".mp3"):
                        ready_to_convert = True
                        download_file = file

            self._add_track_metadata(track_data, download_file)
