def format_messages(messages: list[tuple[str, str]]) -> str:
    """
    messages: [(role, content), ...]
    """
    lines = []

    for role, content in messages:
        if role == "user":
            lines.append(f"User: {content}")
        elif role == "assistant":
            lines.append(f"Assistant: {content}")
        elif role == "summary":
            lines.append(f"Summary of previous conversation:\n{content}")

    return "\n".join(lines)
