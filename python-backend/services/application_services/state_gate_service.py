import os
from services.application_services.video_state_management_service import (
    get_video_state,
    STATUS_PROCESSING,
    STATUS_READY,
    STATUS_FAILED
)

VECTOR_STORE = "vector_store"


def vector_store_exists(videoId: str) -> bool:
    """
        Returns the vector store exists or Not
    """
    persist_path = os.path.join(VECTOR_STORE, videoId)
    return os.path.exists(persist_path)


def current_state(videoId: str):
    """
        Return the current state as PROCESSING | READY | FAILED
    """
    state = get_video_state(videoId)

    if state is None:
        return {
            "status" : "NOT_FOUND",
            "message" : "Video not processed yet"
        }


    if state.status == STATUS_FAILED:
        return {
            "status" : "FAILED",
            "message" : "video processing failed",
            "error" : state.error
        }


    if state.status == STATUS_PROCESSING:
        return {
            "status" : "PROCESSING",
            "message" : "video is being processed"
        }


    if state.status == STATUS_READY and not vector_store_exists(videoId):
        return {
            "status" : "FAILED",
            "message" : "vector store not found"
        }

    return None # state is READY
