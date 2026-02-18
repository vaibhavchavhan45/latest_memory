from typing import List, Dict

def text_splitting(transcript: List) -> List[Dict]:
    """
    Split transcript into chunks with video timestamps.
    """
    total_text = " ".join(item.text for item in transcript)
    total_length = len(total_text)

    # Adaptive chunking
    if total_length <= 6000:
        chunk_size = 400
    elif total_length <= 14000:
        chunk_size = 500
    elif total_length <= 25000:
        chunk_size = 600
    elif total_length <= 35000:
        chunk_size = 800
    else:
        chunk_size = 1000

    chunks = []
    buffer_text = []
    buffer_length = 0
    buffer_start_time = None
    buffer_end_time = None
    chunk_number = 0

    for item in transcript:
        text = item.text.strip()
        if not text:
            continue
        
        # start time for first chunk
        if not buffer_text:
            buffer_start_time = item.start

        buffer_text.append(text)
        buffer_length += len(text)
        buffer_end_time = item.start + item.duration

        # create chunk when size reached
        if buffer_length >= chunk_size:
            chunks.append({
                "text" : " ".join(buffer_text),
                "start_time" : buffer_start_time,
                "end_time" : buffer_end_time,
                "chunk_number" : chunk_number
            })

            chunk_number += 1

            # overlap for new chunk
            buffer_text = [text]
            buffer_length += len(text)
            buffer_start_time = item.start
            buffer_end_time = item.start + item.duration
    
    # Fallback for last buffer
    if buffer_text:
        chunks.append({
           "text" : " ".join(buffer_text),
            "start_time" : buffer_start_time,
            "end_time" : buffer_end_time,
            "chunk_number" : chunk_number 
        })

    return chunks


