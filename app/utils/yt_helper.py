import os
from yt_dlp import YoutubeDL

def extract_info(url: str):
    """
    Ambil metadata + semua kualitas video yang tersedia dari YouTube.
    Menggunakan cookies dari ENV jika tersedia (untuk bypass age/captcha).
    """
    cookies = os.getenv("YT_COOKIES")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
    }

    # Jika ada cookies di environment → tulis sementara di /tmp
    if cookies:
        cookie_file = "/tmp/cookies.txt"
        with open(cookie_file, "w") as f:
            f.write(cookies)
        ydl_opts["cookiefile"] = cookie_file

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Ambil semua format video
        formats = []
        for f in info.get("formats", []):
            # Hanya video (tidak termasuk audio-only)
            if f.get("vcodec") != "none":
                formats.append({
                    "format_id": f.get("format_id"),
                    "resolution": f.get("format_note"),  # contoh: "1080p"
                    "ext": f.get("ext"),
                    "filesize": f.get("filesize"),
                    "url": f.get("url")
                })

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "formats": formats
        }
