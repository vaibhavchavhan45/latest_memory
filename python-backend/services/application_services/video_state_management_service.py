from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import VideoState

STATUS_PROCESSING = "PROCESSING"
STATUS_READY = "READY"
STATUS_FAILED = "FAILED"

def create_new_session():
    """
        Create new session for the database
    """
    return SessionLocal()



def increment_retry_count(videoId: str):
    """
        Increment retry count for retry logic
    """
    db = SessionLocal()
    try:
        state = db.query(VideoState).filter_by(video_id=videoId).first()
        if state:
            state.retry_count = (state.retry_count or 0) + 1
            db.commit()
    finally:
        db.close()



def set_video_state(videoId: str, status: str, languages: str,  error: str = None):
    """
        Create new video state or update existing one with given status and error
    """
    db: Session = create_new_session()

    try:
        state = db.query(VideoState).filter(
            VideoState.video_id == videoId
        ).first()

        if state:
            state.status = status
            state.error = error
            state.languages = languages
        
        else:
            state = VideoState(
                video_id = videoId,
                status = status,
                languages = languages if languages else "en",
                error = error
            )
            db.add(state)

        db.commit()
    
    finally:
        db.close()
        
        
def get_video_state(videoId: str):
    """
        Fetch video state from database by video ID, returns VideoState object or None
    """
    db: Session = create_new_session()

    try:
        return db.query(VideoState).filter(
            VideoState.video_id == videoId
        ).first()

    finally:
        db.close()
        