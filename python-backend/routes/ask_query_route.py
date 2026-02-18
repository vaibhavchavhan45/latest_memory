from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from services.application_services.query_rag_executor_service import execute_rag_flow
from services.application_services.query_state_handler_service import handle_video_state

router = APIRouter()


# pydantic schema
class AskQuery(BaseModel):
    videoId: str
    question: str
    languages: str


@router.post('/query')
def ask_question(data: AskQuery, background_tasks: BackgroundTasks):
    print("Video Id received : ", data.videoId)
    print("Question received : ", data.question)
    print("Language received : ", data.languages)

    # Handles NOT_FOUND, PROCESSING, READY
    state_result = handle_video_state(data.videoId, data.languages, background_tasks)

    # state is not READY return the state
    if (state_result is not None): 
        return state_result

    # state is READY execute the RAG flow
    return execute_rag_flow(data.videoId, data.question)
    