from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models import VideoState
from services.application_services.video_state_management_service import (
    STATUS_FAILED,
    STATUS_PROCESSING
)


def get_failed_videos(limit: int):
    """
        Get small batch of Failed state videos for repair
    """

    db: Session = SessionLocal()

    try:
        failed_videos = (
            db.query(VideoState)
            .filter(VideoState.status == STATUS_FAILED)
            .order_by(VideoState.updated_at.desc())
            .limit(limit)
            .all()
        )
        
        result = []
        for item in failed_videos:
            item.status = STATUS_PROCESSING
            result.append((item.video_id, item.languages))

        db.commit()
        return result

    finally:
        db.close()