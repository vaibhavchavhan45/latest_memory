from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableSequence,
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough
)

from services.core_rag.embedding_service import create_embeddings
from services.core_rag.vector_store_service import load_chroma_index
from config import GROQ_API_KEY
import os

from services.core_rag.rag_filters_service import (
    deduplicate_text,
    apply_token_limit
)
from services.core_rag.rag_reranker_service import rerank_documents
from services.core_rag.rag_formatter_service import format_docs_with_metadata




# RAG flow from embedding to final_chain
def build_rag_chain(videoId: str):
    """
    Builds and returns a Runnable chain:
    Flow : retriever | deduplication | token_limit | format_docs_metadata | prompt | LLM | parser
    """

    embedding_model = create_embeddings()

    try:
        vector_store = load_chroma_index(videoId, embedding_model)
    except Exception as e:
        raise ValueError(f"Vector store not found for video {videoId}. Process video first.")

    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            "fetch_k" : 12,
            "k" : 6,
            "lambda_mult" : 0.5
        } 
    )

    template = PromptTemplate(
    template = """You are a helpful AI assistant specialized in answering questions about YouTube video content.

    Your task is to provide accurate, concise answers based STRICTLY on the provided video transcript context.

    CRITICAL RULES:
    1. Answer ONLY using information from the context below
    2. Do NOT use any external knowledge or make assumptions
    3. If the answer is not in the context, respond: "I couldn't find this information in the video."
    4. Be direct and concise - avoid unnecessary elaboration
    5. DO NOT add meta-commentary like "according to the video", "as presented in the transcript", "based on the context", or similar phrases
    6. Write as if YOU are explaining directly to the user, not referring to a third-party source
    7. Answer in a natural, conversational tone without mentioning the transcript or video
    8. Always maintain a polite, professional, and respectful tone regardless of how the user phrases their question
    9. If the user uses inappropriate language or behaves rudely, respond calmly and professionally without matching their tone
    10. Never use offensive, rude, or inappropriate language in your responses

    Conversation so far:
    {chat_history}

    Context:
    {context}

    User Question:
    {question}

    Answer:
    """,
    input_variables = ['chat_history', 'context', 'question']
    )

    model = ChatOpenAI(
        model = 'openai/gpt-oss-120b',
        openai_api_key = os.getenv('GROQ_API_KEY'),
        openai_api_base = 'https://api.groq.com/openai/v1'
    )

    parser = StrOutputParser()

    # chain structure
    shared_pipeline = RunnableSequence(
        retriever,
        RunnableLambda(deduplicate_text),
    )

    input_chain = RunnableParallel({
    "data": RunnableSequence(
        RunnableLambda(lambda x: x["question"] if isinstance(x, dict) else x),  # ✅ Extract question
        shared_pipeline
    ),
    "question": RunnableLambda(lambda x: x["question"] if isinstance(x, dict) else x)  # ✅ Extract question
    })

    data_chain = RunnableSequence(
        input_chain,
        RunnableLambda(lambda x: rerank_documents(x["question"], x["data"])),
        RunnableLambda(apply_token_limit),
        RunnableLambda(format_docs_with_metadata),
    )

    final_input_chain = RunnableParallel({
        "data" : data_chain,
        "question" : RunnablePassthrough(),
        "chat_history" : RunnablePassthrough()
    })

    llm_chain = RunnableSequence(
        RunnableLambda(lambda x: {
            "chat_history" : x.get("chat_history", ""),
            "context" : x["data"]["context"],
            "question" : x["question"]
        }),
        template,
        model,
        parser
    )

    metadata_chain = RunnableLambda(
        lambda x: x["data"] ["docs"]
    )

    final_chain = RunnableSequence(
        final_input_chain,
        RunnableParallel({
            "response" : llm_chain,
            "metadata" : metadata_chain
        })
    )

    return final_chain