import os
from langchain_chroma import Chroma
from langchain_core.documents import Document

BASE_DIR = "vector_store"

# If embedding already exist then don't add new ones in that folder
def check_embeddings_exist(videoId: str):
    '''
        Embeddings of the video already exist in vector store
    '''
    persist_path = os.path.join(BASE_DIR, videoId)
    return os.path.exists(persist_path)


# chunks to embedding conversion
def save_chunks_to_chroma(chunks, embedding, videoId: str):
    # # Create the folder path where embeddings will be saved: "vector_store/videoId"
    # persist_path = os.path.join(BASE_DIR, videoId)

    # # Create the folder on disk (if it doesn't exist already)
    # os.makedirs(persist_path, exist_ok = True)
   
    # # convert text to chunks and add to Chroma db
    # vector_store = Chroma.from_documents(
    #     documents = chunks,
    #     embedding = embedding_model,
    #     persist_directory = persist_path # Where to save the database
    # )

    # # Return the folder path where embeddings were saved
    # return persist_path

    persist_path = os.path.join(BASE_DIR, videoId)
    os.makedirs(persist_path, exist_ok = True)

    documents = []

    for item in chunks:
        documents.append(
            Document(
                page_content = item["text"],
                metadata = {
                    "start_time" : item["start_time"],
                    "end_time" : item["end_time"],
                    "chunk_number" : item["chunk_number"],
                    "video_id" : videoId,
                    "source" : "Youtube"
                }
            )
        )

    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embedding,
        persist_directory = persist_path
    )

    return persist_path




# Load saved embeddings from disk and return searchable vector store
def load_chroma_index(videoId: str, embedding_model):
    # Create the folder path where embeddings are saved: "vector_store/videoId"
    persist_path = os.path.join(BASE_DIR, videoId)

    # Check if the folder exists - if not, embeddings were never created
    if not os.path.exists(persist_path):
        raise Exception("Chroma index not found for this video")

    # Load the Chroma database from the saved folder using the same embedding model
    vector_store = Chroma(
        persist_directory = persist_path,  # Folder where embeddings are stored
        embedding_function = embedding_model # same embedding model
    )

    # return the vector store of that videoId
    return vector_store 
    
