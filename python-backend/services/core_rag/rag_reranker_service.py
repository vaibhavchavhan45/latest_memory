from typing import List
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


reranker = None

def lazy_load_reranker():
    """Lazy load the re-ranker for the first use"""
    global reranker
    if reranker is None:
        reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return reranker



def rerank_documents(question: str, docs: List[Document]) -> List[Document]:
    """Re-ranks documents by relevance to query using CrossEncoder"""
    extract_text = []
    for item in docs:
        extract_text.append(item.page_content)
    
    reranker = lazy_load_reranker()
    reranked_results = reranker.rank(
        question,
        extract_text,
        return_documents = False
    )

    reranked_docs = []
    for item in reranked_results:
        index = item['corpus_id']
        doc = docs[index]
        reranked_docs.append(doc)
    
    return reranked_docs