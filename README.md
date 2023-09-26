# YouTubeDownloader
Python script for downloading music from YouTube. 

# Installation
Clone the repository:
```
git clone https://github.com/StudentPP1/YouTubeDownloader.git
```

Install the required packages:
```
pip install -r requirements.txt
```

run:
```
python main.py
```

# Usage
You can download the audio file from one video or download the whole playlist at once (if it is not private) 

The downloaded tracks will be saved in the 'Music' folder in the project

# Note
To use the script you need to download [ffmpeg](https://ffmpeg.org/) and add the absolute path to 'ffmpeg.exe' to the code
```
ydl_opts = {'format': 'bestvideo+bestaudio/best',
            "ffmpeg_location": r"your absolute path to 'ffmpeg.exe' "}
```

