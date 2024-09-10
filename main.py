import os
from os import path
from utils.const import destination_path
from spotify.spotify_downloader import Spotify
from youtube.youtube_downloader import YouTube


def main():
    spotify = Spotify()
    youtube = YouTube()

    while True:
        try:
            url = input("Enter the link of video or playlist (q - exit): ")

            if not path.exists(destination_path):
                os.mkdir(destination_path)

            if url == 'q':
                print("See you soon")
                break

            if url.startswith("https://open.spotify.com/playlist"):
                spotify.download_playlist(url)

            elif url.startswith('https://www.youtube.com/watch?'):
                youtube.download_track(url)

            elif url.startswith('https://www.youtube.com/playlist?'):
                youtube.download_playlist(url)

        except Exception as exception:
            print(f"Sorry, loader crashed: {exception}")


if __name__ == "__main__":
    main()
