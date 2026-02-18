from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Index
)
from datetime import datetime

from db.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    # userId_videoId or any session identifier
    session_id = Column(String, nullable=False, index=True)

    # user | assistant | summary
    role = Column(String, nullable=False)

    # actual message text
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# Optional but good for performance
Index("idx_chat_messages_session_id", ChatMessage.session_id)
