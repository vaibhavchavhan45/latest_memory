from services.core_rag.transcript_service import fetch_transcript
from services.core_rag.splitting_service import text_splitting
from services.core_rag.embedding_service import create_embeddings
from services.core_rag.vector_store_service import (
    save_chunks_to_chroma, 
    check_embeddings_exist
)

from services.application_services.video_state_management_service import(
    set_video_state,
    STATUS_PROCESSING,
    STATUS_READY,
    STATUS_FAILED
)

def process_video_service(videoId: str, languages: str):
    print("Starting process video service")
    try:
        print("Inside try")
        # check that embedding are already exist or not
        if check_embeddings_exist(videoId):
            print("embedding exists")
            return {
                "message" : "Video already processed --Embeddings are available in vector store",
                "video_id" : videoId,
                "already_exists" : True,
                "status" : STATUS_READY
            }

        print("setting up state")
        # set the state as processing
        set_video_state(videoId, STATUS_PROCESSING, languages)

        print("before transcript")
        # fetch transcript
        transcript = fetch_transcript(videoId, languages)

        print("Transcript fetched successfully")

        # text splitting
        chunks = text_splitting(transcript)
        print("Total chunks created : ", len(chunks))
        print("Sample chunk : ", chunks[0]["text"])

        # embeddings
        embedding = create_embeddings()
        print("Embeddings model initialised successfully")

        # Save to chroma
        save_path = save_chunks_to_chroma(chunks, embedding, videoId)
        print("Chroma index save at : ", save_path)

        set_video_state(videoId, STATUS_READY, languages)

        return {
            "message" : "transcript fetched successfully",
            "video_id" : videoId,
            "languages" : languages,
            "total_chunks" : len(chunks),
            "chroma_path" : save_path,
            "already_exists" : False,
            "status" : STATUS_READY
        }

    except Exception as e:
        print(e)
        set_video_state(videoId, STATUS_FAILED, languages, str(e))
        return{
            "status" : STATUS_FAILED,
            "error" : str(e),
            "video_id" : videoId
        }
