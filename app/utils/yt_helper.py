from yt_dlp import YoutubeDL

def extract_info(url: str):
    """
    Ambil metadata + semua kualitas video yang tersedia dari YouTube.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Ambil semua format video (bukan hanya yang best)
        formats = []
        for f in info.get("formats", []):
            if f.get("vcodec") != "none":  # pastikan hanya video (bukan audio)
                formats.append({
                    "format_id": f.get("format_id"),
                    "resolution": f.get("format_note"),  # misalnya "1080p"
                    "ext": f.get("ext"),
                    "filesize": f.get("filesize"),
                    "url": f.get("url")
                })

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "formats": formats  # <== ini list semua resolusi
        }
