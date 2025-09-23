from yt_dlp import YoutubeDL

def extract_info(url: str, format: str = "bestvideo+bestaudio/best"):
    """
    Extract metadata + direct download URL from YouTube using yt-dlp.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": format,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "url": info["url"],
            "ext": info.get("ext", "mp4"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
        }
