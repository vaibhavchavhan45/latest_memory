from typing import List
from langchain_core.documents import Document


def format_docs_with_metadata(docs: List[Document]) -> dict:
    """
        Formats documents with timestamps for LLM context.
        Returns a single string with each chunk showing when it appears in the video.
    """
    formatted_context_text = []
    for item in docs:
        start_time = item.metadata.get("start_time", "start_time doesn't exists")
        end_time = item.metadata.get("end_time", "end_time doesn't exists")
        formatted_context_text.append(
            f"[{start_time} - {end_time}] {item.page_content}"
        )

    return {
        "context" : "\n\n".join(formatted_context_text),
        "docs" : docs
    }