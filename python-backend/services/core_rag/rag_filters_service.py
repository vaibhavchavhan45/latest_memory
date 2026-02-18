from typing import List
from langchain_core.documents import Document


MAX_CONTEXT_CHARS = 5000


def deduplicate_text(docs: List[Document]) -> List[Document]:
    """
    Remove duplicate chunks so LLM doesn't see repeated content
    """
    already_processed_text = set()
    unique_docs = []
    for item in docs:
        text = item.page_content.strip()
        if text not in already_processed_text:
            already_processed_text.add(text)
            unique_docs.append(item)
    return unique_docs



def apply_token_limit(docs: List[Document], max_chars: int = MAX_CONTEXT_CHARS) -> List[Document]:
    """
        Limit context to {MAX_CONTEXT_CHARS} chars so LLM can process documents without overloading
    """
    final_docs = []
    total_length = 0
    for item in docs:
        length = len(item.page_content)
        if total_length + length > max_chars:
            break
        final_docs.append(item)
        total_length += length
    return final_docs