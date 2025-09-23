from fastapi import APIRouter, Query
from app.utils.yt_helper import extract_info

router = APIRouter()

@router.get("/extract")
async def extract_url(url: str = Query(..., description="YouTube URL")):
    """
    Endpoint untuk ambil direct link dari YouTube video.
    """
    try:
        data = extract_info(url)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
