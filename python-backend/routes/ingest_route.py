from fastapi import APIRouter
import asyncio
from pydantic import BaseModel

from services.video_repair.get_failed_video_service import get_failed_videos
from services.video_repair.video_repair_worker import repair_video


router = APIRouter()


# Ingest route
@router.post('/process-video')
def process_video():
    failed_videos = get_failed_videos(limit = 5)

    if not failed_videos:
        return {
            "message" : "No Failed videos found"
        }

    for video_id, languages in failed_videos:
        asyncio.create_task(repair_video(video_id, languages))

    return {
        "message" : "Processing starts for Failed videos"
    }

    