from fastapi import HTTPException

def query_validator(question: str) -> str:
    """
        Validate the user question by removing extra spaces and length
    """
    question = question.strip()

    if not question or len(question) == 0:
        raise HTTPException(
            status_code = 400,
            detail = "Question prompt cannot be empty"
        )

    if len(question) > 5000:
        raise HTTPException(
            status_code = 400,
            detail = "Question is too long, Please try to be more concise or break it into smaller questions. "
        )

    return question