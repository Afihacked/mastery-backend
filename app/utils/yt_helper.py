from yt_dlp import YoutubeDL

def extract_info(url: str):
    """
    Ambil metadata + semua kualitas video dari YouTube.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
        "noplaylist": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Ambil semua format video
    formats = []
    for f in info.get("formats", []):
        if f.get("vcodec") != "none":  # hanya ambil format yang ada video
            formats.append({
                "format_id": f.get("format_id"),
                "resolution": f.get("format_note") or f.get("height"),
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
