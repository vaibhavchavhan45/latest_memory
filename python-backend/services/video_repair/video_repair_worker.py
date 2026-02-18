import asyncio

from services.application_services.video_processing_service import process_video_service
from services.application_services.video_state_management_service import (
    set_video_state,
    STATUS_FAILED
)


async def repair_video(videoId: str, languages: str):
    """
        Re-process the failed video safely
    """

    try:
        await asyncio.to_thread(
            process_video_service,
            videoId,
            languages
        )

        print(f"Auto-repair complete for the video Id {videoId}")
    
    except Exception as e:
        print(f"Auto-repair failed for the video Id {videoId}")
        await asyncio.to_thread(set_video_state, videoId, STATUS_FAILED, languages, str(e))
        raise

