from fastapi import APIRouter, Query
from app.utils.yt_helper import extract_info

router = APIRouter()

@router.get("/convert")
async def convert_audio(url: str = Query(...)):
    """
    Ambil hanya audio (format mp3/m4a).
    """
    try:
        data = extract_info(url, format="bestaudio/best")
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
