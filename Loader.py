from pytube import YouTube
from pytube import Playlist
import requests
import subprocess
import eyed3
import os

VIDEO_NAME = 'video.mp4'
AUDIO_NAME = 'video.mp3'


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

    title = yt.title.replace('-', '')
    author = yt.author
    if author in title:
        title = title.replace(author, '').strip()
    video_id = url[url.index("=") + 1:url.index("&")]
    with open("img.jpg", 'wb') as f:
        img = requests.get(f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg').content
        f.write(img)

    audio_best = streams.filter(only_audio=True).desc().first()
    audio_best.download(filename=VIDEO_NAME)
    return author, title


def load_metadata_to_mp3(file_mp3, artist, title):
    audio_file = eyed3.load(file_mp3)
    audio_file.tag.artist = artist
    audio_file.tag.title = title
    audio_file.tag.images.set(3, open('img.jpg', 'rb').read(), 'image/jpeg')
    audio_file.tag.save()
    os.rename(file_mp3, f'{artist} - {title}.mp3')
    return f'{artist} - {title}.mp3'


def del_files():
    for i in os.listdir():
        if i.endswith('.jpg'):
            os.remove(i)
        elif i.endswith('.mp4'):
            os.remove(i)


def main():
    while True:
        try:
            url = input('Enter the link of video or playlist (q - exit): ')
            if url == 'q':
                print("See you soon")
                break
            elif 'https://www.youtube.com/watch?' in url:
                print("Downloading video...")
                author, title = download_video(url)
                print("Converting video to audio...")
                convert_video_to_audio_ffmpeg(VIDEO_NAME)
                print("Loading metadata to audio...")
                music_file = load_metadata_to_mp3(AUDIO_NAME, author, title)
                print("Deleting other files...")
                del_files()
                print(f"Done: {music_file}")
            elif 'playlist' in url:
                videos = Playlist(url)
                for video_url in videos.video_urls:
                    print("Downloading video...")
                    author, title = download_video(video_url)
                    print("Converting video to audio...")
                    convert_video_to_audio_ffmpeg(VIDEO_NAME)
                    print("Loading metadata to audio...")
                    music_file = load_metadata_to_mp3(AUDIO_NAME, author, title)
                    print("Deleting other files...")
                    del_files()
                    print(f"Done: {music_file}")
            else:
                print("Enter the link of video, please...")
                continue
        except Exception as ex:
            print(ex)
            print("Sorry... Try again")


if __name__ == '__main__':
    main()
