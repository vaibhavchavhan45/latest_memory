from fastapi import BackgroundTasks

from services.application_services.video_processing_service import process_video_service
from services.application_services.state_gate_service import current_state
from services.application_services.video_state_management_service import (
    get_video_state,
    set_video_state,
    increment_retry_count
)


def handle_video_state(videoId: str, languages: str, background_tasks: BackgroundTasks):
    """
        Check video state and handle NOT_FOUND, PROCESSING, FAILED states.
        return the immediately with the presnt state
    """

    state_response = current_state(videoId)
    print("State response:", state_response)

    # NOT_FOUND state
    if state_response and state_response["status"] == "NOT_FOUND":
        print("NOT_FOUND → starting background processing")

        background_tasks.add_task(
            process_video_service,
            videoId,
            languages
        )

        return {
            "status": "PROCESSING",
            "message": "Video not processed yet. Processing started."
        }


    # PROCESSING state
    if state_response and state_response["status"] == "PROCESSING":
        print("PROCESSING, checking DB")

        db_state = get_video_state(videoId)

        if db_state and db_state.status == "READY":
            print("PROCESSING is READY, continue to RAG")
            pass
             
        else:
            print("Still PROCESSING")
            return {
                "status": "PROCESSING",
                "message": "Video is still being processed. Please wait."
            }


    # FAILED state
    if state_response and state_response["status"] == "FAILED":
        db_state = get_video_state(videoId)
        retry_count = db_state.retry_count or 0

        print(f"FAILED → retry_count={retry_count}")

        if retry_count < 2:
            print("Retrying video processing")

            print("before increment")
            increment_retry_count(videoId)
            print("after increment")

            set_video_state(
                videoId,
                status="PROCESSING",
                languages = languages,
                error = None
            )
            print("after video state")

            background_tasks.add_task(
                process_video_service,
                videoId,
                languages
            )
            print("after bg tasks")

            return {
                "status": "PROCESSING",
                "message": f"Retrying video processing ({retry_count + 1}/2)"
            }

        # 2 retries (after that permanenet failed msg)
        return {
            "status": "FAILED",
            "message": "Video processing failed after multiple retries. Cannot process this video."
        }

    # READY state
    return None 