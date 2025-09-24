import os
from yt_dlp import YoutubeDL, DownloadError

def extract_info(url: str, format: str = None):
    """
    Ambil metadata + semua kualitas video/audio dari YouTube.
    Bisa dibatasi format tertentu (contoh: 'bestaudio/best').
    """
    cookies = os.getenv("YT_COOKIES")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
        "nocheckcertificate": True,
        "ignoreerrors": True,   # jangan crash kalau video unavailable
        "noplaylist": True,

        # ⚡ Anti-429
        "sleep_interval": 2,         # jeda antar request
        "max_sleep_interval": 5,     # acak delay max 5 detik
        "throttled_rate": 1000000,   # batasi speed (1 MB/s biar ga dianggap bot)

        # ⚡ Bypass deteksi bot dengan UA + extractor args
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0 Safari/537.36"
        },
        "extractor_args": {
            "youtube": {
                "player_client": ["web"]  # bisa dicoba "android", "tv" juga
            }
        }
    }


    # Jika ada cookies di environment → tulis sementara di /tmp
    if cookies:
        cookie_file = "/tmp/cookies.txt"
        with open(cookie_file, "w") as f:
            f.write(cookies)
        ydl_opts["cookiefile"] = cookie_file

    # Kalau user minta format tertentu (misalnya audio)
    if format:
        ydl_opts["format"] = format

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                return {"success": False, "error": "Tidak bisa mengambil info video."}

            # Kalau format audio saja → langsung return URL audio
            if format:
                return {
                    "success": True,
                    "title": info.get("title"),
                    "thumbnail": info.get("thumbnail"),
                    "duration": info.get("duration"),
                    "url": info.get("url"),  # link direct audio
                    "ext": info.get("ext")
                }

            # Default: return semua format video/audio
            formats = []
            for f in info.get("formats", []):
                if f.get("url"):
                    formats.append({
                        "format_id": f.get("format_id"),
                        "resolution": f.get("format_note") or f.get("height"),
                        "ext": f.get("ext"),
                        "filesize": f.get("filesize"),
                        "url": f.get("url")
                    })

            return {
                "success": True,
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "formats": formats
            }

    except DownloadError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Unknown error: {str(e)}"}
