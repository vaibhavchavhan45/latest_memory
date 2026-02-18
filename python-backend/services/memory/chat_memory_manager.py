from services.memory.chat_memory_repository import ChatMemoryRepository
from services.memory.chat_memory_formatter import format_messages
from services.memory.chat_memory_summarizer import summarize_text
from services.memory.chat_token_utils import estimate_tokens


MAX_CHAT_TOKENS = 3000
SUMMARY_TRIGGER_TOKENS = 2000


class ChatMemoryManager:
    def __init__(self):
        self.repo = ChatMemoryRepository()

    def load_history(self, session_id: str) -> str:
        messages = self.repo.fetch_messages(session_id)
        return format_messages(messages)

    def save_user_message(self, session_id: str, text: str):
        self.repo.save_message(session_id, "user", text)

    def save_ai_message(self, session_id: str, text: str):
        self.repo.save_message(session_id, "assistant", text)

    def maybe_summarize(self, session_id: str):
        messages = self.repo.fetch_messages(session_id)
        formatted = format_messages(messages)
        tokens = estimate_tokens(formatted)

        if tokens < SUMMARY_TRIGGER_TOKENS:
            return

        summary = summarize_text(formatted)
        self.repo.replace_with_summary(session_id, summary)

    def is_chat_valid(self, session_id: str) -> bool:
        messages = self.repo.fetch_messages(session_id)
        tokens = estimate_tokens(format_messages(messages))
        return tokens < MAX_CHAT_TOKENS
