import os
import logging
from yt_dlp import YoutubeDL, DownloadError

# Optional: aktifkan logging untuk debugging (hapus/ubah saat production)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("yt_helper")

def extract_info(url: str, format: str = None):
    """
    Ambil metadata + semua kualitas video/audio dari YouTube.
    Bisa dibatasi format tertentu (misal 'bestaudio/best').

    Membaca:
      - YT_COOKIES (isi file cookies.txt dalam format Netscape)
      - PROXY_URL  (opsional, contoh: http://user:pass@host:port atau socks5://host:port)
      - PLAYER_CLIENT (opsional, "web" / "android" / "tv")
    """
    cookies = os.getenv("YT_COOKIES")
    proxy = os.getenv("PROXY_URL")
    player_client = os.getenv("PLAYER_CLIENT", "web")  # default "web"

    # dasar options
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "noplaylist": True,
        # anti-429 / rate-limit mitigation
        "sleep_interval": 2,
        "max_sleep_interval": 5,
        "throttled_rate": 1000000,   # 1 MB/s
        # headers & extractor args
        "http_headers": {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
        },
        "extractor_args": {
            "youtube": {
                "player_client": [player_client]
            }
        },
        # jangan terlalu agresif retry di yt-dlp (tapi kita tangani exception)
    }

    # tulis cookies ke /tmp jika ada
    cookie_file = None
    if cookies:
        cookie_file = "/tmp/cookies.txt"
        try:
            with open(cookie_file, "w") as f:
                f.write(cookies)
            ydl_opts["cookiefile"] = cookie_file
            logger.info("YT cookies written to %s", cookie_file)
        except Exception as e:
            logger.exception("Gagal tulis cookie file: %s", e)

    # proxy jika diset
    if proxy:
        ydl_opts["proxy"] = proxy
        logger.info("Proxy enabled: %s", proxy)

    # format request (mis: 'bestaudio/best')
    if format:
        ydl_opts["format"] = format

    try:
        # untuk debugging lokal, kamu bisa set quiet=False
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                # Beri pesan lebih jelas untuk debug
                logger.warning("extract_info returned None for URL: %s", url)
                return {"success": False, "error": "Tidak bisa mengambil info video (info is None). Mungkin kena 429 atau cookies invalid."}

            # Kalau hanya audio diminta
            if format:
                return {
                    "success": True,
                    "title": info.get("title"),
                    "thumbnail": info.get("thumbnail"),
                    "duration": info.get("duration"),
                    "url": info.get("url"),
                    "ext": info.get("ext")
                }

            # Default: list semua format
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
        # yt-dlp specific exceptions, beri pesan yang jelas
        msg = str(e)
        logger.error("DownloadError: %s", msg)
        if "429" in msg or "Too Many Requests" in msg:
            return {"success": False, "error": "429 Too Many Requests — IP kemungkinan dibatasi. Pertimbangkan proxy atau ganti host."}
        if "Sign in to confirm" in msg or "cookies" in msg.lower():
            return {"success": False, "error": "YouTube meminta sign-in / cookies invalid. Pastikan YT_COOKIES valid (gunakan --cookies-from-browser atau export full cookies.txt)."}
        return {"success": False, "error": msg}

    except Exception as e:
        logger.exception("Unknown exception in extract_info")
        return {"success": False, "error": f"Unknown error: {str(e)}"}
