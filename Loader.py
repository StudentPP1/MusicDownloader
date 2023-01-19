from pytube import YouTube
from pytube import Playlist
import requests
import subprocess
import eyed3
import os
import re

VIDEO_NAME = "video.mp4"
AUDIO_NAME = "video.mp3"
PATH = "Loaded music\\"


def convert_video_to_audio_ffmpeg(video_file, output_ext="mp3"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)


def download_video(url):
    yt = YouTube(url)
    streams = yt.streams

    title = re.sub(r"[^А-Яа-яA-Za-z0-9 ]", '', yt.title).strip()
    author = re.sub(r"[^А-Яа-яA-Za-z0-9 ]", '', yt.author).strip()
    if author in title:
        title = title.replace(author, '').strip()
    if "&" in url:
        video_id = url[url.index("=") + 1:url.index("&")]
    else:
        video_id = url[url.index("=") + 1:]
    with open("img.jpg", 'wb') as f:
        img = requests.get(f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg').content
        f.write(img)

    video = streams.filter(file_extension='mp4').desc().first()
    video.download(PATH, filename=VIDEO_NAME)
    return author, title


def load_metadata_to_mp3(file_mp3, artist, title):
    audio_file = eyed3.load(file_mp3)
    audio_file.tag.artist = artist
    audio_file.tag.title = title
    audio_file.tag.images.set(3, open('img.jpg', 'rb').read(), 'image/jpeg')
    audio_file.tag.save()
    os.rename(f"{file_mp3}", f'{PATH}{artist} - {title}.mp3')
    return f'{PATH}{artist} - {title}.mp3'


def del_files():
    for i in os.listdir():
        if i.endswith('.jpg'):
            os.remove(i)
    for i in os.listdir(PATH):
        if i.endswith('.mp4'):
            os.remove(PATH+i)


def main():
    while True:
        try:
            url = input('Enter the link of video or playlist (q - exit): ')
            if url == 'q':
                print("See you soon")
                break
            elif url.startswith('https://www.youtube.com/watch?'):
                print("Downloading video...")
                author, title = download_video(url)
                print("Converting video to audio...")
                convert_video_to_audio_ffmpeg(PATH + VIDEO_NAME)
                print("Loading metadata to audio...")
                music_file = load_metadata_to_mp3(PATH + AUDIO_NAME, author, title)
                print("Deleting other files...")
                del_files()
                print(f"Done: {music_file}")
            elif url.startswith('https://www.youtube.com/playlist?'):
                print("Getting playlist...")
                videos = Playlist(url)
                video_urls = [video_url for video_url in videos.video_urls]
                for video_url in video_urls:
                    log = f"{video_urls.index(video_url) + 1}/{len(video_urls)}"
                    print(f"Downloading {log} video...")
                    author, title = download_video(video_url)
                    print(f"Converting {log} video to audio...")
                    convert_video_to_audio_ffmpeg(PATH + VIDEO_NAME)
                    print("Loading metadata to audio...")
                    music_file = load_metadata_to_mp3(PATH + AUDIO_NAME, author, title)
                    print("Deleting other files...")
                    del_files()
                    print(f"Done: {music_file}")
            else:
                print("Enter the link of video or playlist, please...")
                continue
        except Exception as ex:
            print(ex)
            print("Sorry... Try again")


if __name__ == '__main__':
    main()
