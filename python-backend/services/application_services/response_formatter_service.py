import re
from typing import Optional

def standard_timestamp(seconds: str) -> str:
    """
        Convert timestamp to {hrs:mins:secs} format
    """
    if seconds is None:
        return ""
    
    seconds = int(seconds)
    hrs = seconds // 3600
    min = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs : 02d} : {min : 02d} : {secs : 02d}"


def clean_llm_response_text(text: Optional[str]) -> str:
    """
        Cleaning up the LLM's response in readable format
    """
    if not text:
        return ""
    
    text = text.replace("\\n", "\n")

    text = re.sub(r"【[^】]*】", "", text)

    text = re.sub(r"\(≈[^)]*\)", "", text)

    text = re.sub(r"\[\d+\]", "", text)

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r'"\s+([^"]*)\s+"', r'"\1"', text)

    return text.strip()
        

def format_answer_payload(
    llm_response: str, 
    start_time: Optional[float] = None, 
    end_time: Optional[float] = None
) -> dict:

    """Final API response builder"""
    payload = {
        "answer" : clean_llm_response_text(llm_response)
    }
    if start_time is not None:
        payload["start_time"] = start_time
    if end_time is not None:
        payload["end_time"] = end_time

    return payload