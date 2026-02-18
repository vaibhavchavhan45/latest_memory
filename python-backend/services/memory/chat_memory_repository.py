from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.chat_memory_schema import ChatMessage


class ChatMemoryRepository:
    def __init__(self):
        self.db: Session = SessionLocal()

    def save_message(self, session_id: str, role: str, content: str):
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content
        )
        self.db.add(message)
        self.db.commit()

    def fetch_messages(self, session_id: str):
        return (
            self.db.query(ChatMessage.role, ChatMessage.content)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    def replace_with_summary(self, session_id: str, summary: str):
        (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .delete()
        )

        summary_msg = ChatMessage(
            session_id=session_id,
            role="summary",
            content=summary
        )

        self.db.add(summary_msg)
        self.db.commit()
