from fastapi import HTTPException 

from services.core_rag.rag_chain_service import build_rag_chain
from services.application_services.user_query_validation_service import query_validator
from services.application_services.response_formatter_service import (
    format_answer_payload, 
    clean_llm_response_text
)
from services.memory.chat_memory_manager import ChatMemoryManager

def execute_rag_flow(videoId: str, question: str, userId: str = "default_user"):
    """
        Executing the RAG flow for the READY state
    """

    print("state is READY.... executing RAG flow")

    # validate question ONLY when ready
    question = query_validator(question)
    print("received question now")

    session_id = f"{userId}_{videoId}"
    print(session_id, "This is my session id")
    memory = ChatMemoryManager()
    print("After memory management")

    # token limit check BEFORE doing anything
    if not memory.is_chat_valid(session_id):
        print("Chat not valid")
        raise HTTPException(
            status_code=400,
            detail="Chat history limit reached. Please start a new chat."
        )
    print("after chat, before try")

    try:
        print("Inside try")
        # load chat history FIRST (does NOT include current question)
        chat_history = memory.load_history(session_id)
        print("After chat history", chat_history)

        rag_chain = build_rag_chain(videoId)
        print("After rag chain")

        retrieval_question = f"{chat_history}\nUser: {question}" if chat_history else question

        result = rag_chain.invoke({
            "question": retrieval_question,
            "chat_history": chat_history
        })
        print("After result", result)

        # save user message AFTER successful invoke
        memory.save_user_message(session_id, question)
        print("After saving user msg")

        # No documents
        if not result["metadata"]:
            cleaned_response = clean_llm_response_text(result["response"])

            # save assistant message
            memory.save_ai_message(session_id, cleaned_response)
            memory.maybe_summarize(session_id)

            return {
                "video_id": videoId,
                "question": question,
                "result": cleaned_response,
                "primary_start_time": None,
                "primary_end_time": None,
                "all_remaining_timestamps": []
            }

        # Documents exist
        first_doc = result["metadata"][0]

        first_doc_start_time = first_doc.metadata.get("start_time", None)
        first_doc_end_time = first_doc.metadata.get("end_time", None)

        formatted_llm_response = format_answer_payload(
            llm_response=result["response"],
            start_time=first_doc_start_time,
            end_time=first_doc_end_time
        )

        # save assistant message
        memory.save_ai_message(session_id, formatted_llm_response["answer"])
        memory.maybe_summarize(session_id)

        remaining_timestamps = []

        if len(result["metadata"]) > 1:
            for i, item in enumerate(result["metadata"]):
                if i == 0:
                    continue
                remaining_timestamps.append({
                    "start_time": item.metadata.get("start_time", None),
                    "end_time": item.metadata.get("end_time", None)
                })

        return {
            "video_id": videoId,
            "question": question,
            "result": formatted_llm_response["answer"],
            "primary_start_time": formatted_llm_response["start_time"],
            "primary_end_time": formatted_llm_response["end_time"],
            "all_remaining_timestamps": remaining_timestamps
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing query")