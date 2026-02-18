from sqlalchemy import (
    Column, 
    Text, 
    String, 
    DateTime, 
    Integer
)
from datetime import datetime
from db.database import Base

class VideoState(Base):
    __tablename__ = "video_states"

    video_id = Column(String, primary_key = True, index = True)
    status = Column(String, nullable = False)
    error = Column(Text, nullable = True)
    languages = Column(Text, nullable = False)
    retry_count = Column(Integer, default=0)

    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(
        DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow
    )