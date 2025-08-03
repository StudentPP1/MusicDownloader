# 🎵 MusicDownloader

Python script for downloading music from **YouTube** and **Spotify liked tracks** (via YouTube search).  
The downloaded tracks will be saved as `.mp3` with metadata and album covers.

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/StudentPP1/YouTubeDownloader.git
   cd YouTubeDownloader
    ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the project root with the following variables:

   ```env
   CLIENT_ID=""
   SECRET_ID=""
   REDIRECT_URI=http://localhost:8888/callback
   FFMPEG_LOCATION="C:\\absolute\\path\\to\\ffmpeg.exe"
   ```

   * ⚠️ `REDIRECT_URI` must match what's added in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) app settings.
   * 📥 [Download FFmpeg](https://ffmpeg.org/) and set `FFMPEG_LOCATION` to the path of `ffmpeg.exe`.

---

## ▶️ Usage

```bash
python main.py
```

* You will be prompted to enter:

  * A YouTube link (single track or playlist)
  * Or type `liked` to download tracks from your Spotify "Liked Songs"
  * Type `q` to exit

---

## 📁 Output

* All `.mp3` files will be saved into the `Music/` folder with proper metadata:

  * Title, Artist, Album, Release date
  * Album cover image

---

## ⚠️ Notes

To use **Spotify features**:

* You must authorize once via browser (Spotify OAuth2 flow will launch automatically).
* A token will be saved to `token.json` for future use.
