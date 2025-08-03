import sys
import os
import json
import subprocess
from os import path
from time import sleep

from const import destination_path
from spotify_downloader import Spotify
from youtube_downloader import YouTube

# This script is designed to run in a virtual environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def ensure_token():
    if path.exists("token.json"):
        with open("token.json", "r") as f:
            token_data = json.load(f)
            return token_data.get("access_token")
    else:
        print("🔑 No Spotify token found. Launching authorization server...")

        # Ensure the server is run with the same Python executable as this script
        python_executable = sys.executable

        proc = subprocess.Popen([python_executable, "server.py"])
        print("🌐 Please authorize in your browser...")

        while not path.exists("token.json"):
            sleep(1)
        print("✅ Authorization complete. Continuing...")
        proc.terminate()

        with open("token.json", "r") as f:
            token_data = json.load(f)
            return token_data.get("access_token")


def main():
    youtube = YouTube()

    while True:
        try:
            url = input(
                "Enter YouTube link, 'liked' for Spotify likes, or 'q' to exit: "
            )

            if not path.exists(destination_path):
                os.mkdir(destination_path)

            if url == "q":
                print("See you soon")
                break

            if url == "liked":
                token = ensure_token()
                spotify = Spotify(token)
                spotify.download_liked_tracks()

            elif url.startswith("https://www.youtube.com/watch?"):
                youtube.download_track(url)

            elif url.startswith("https://www.youtube.com/playlist?"):
                youtube.download_playlist(url)

        except Exception as exception:
            print(f"❌ Sorry, loader crashed: {exception}")


if __name__ == "__main__":
    main()
