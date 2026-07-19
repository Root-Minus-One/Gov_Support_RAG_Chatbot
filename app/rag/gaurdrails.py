def validate_input(question: str) -> tuple[bool, str]:
    if not question or len(question.strip()) < 10:
        return False, "Input cannot be empty or Question length too short"
    
    if len(question.strip()) > 500:
         return False, "Question too long"
    
    injection_keywords = [
        "ignore previous instructions",
        "system prompt",
        "act as a",
        "you are now a"
    ]

    if any(keyword in question.lower() for keyword in injection_keywords):
        return False, "Potential prompt injection or system override detected."

    return True, "Input is_valid."



def check_relevance(chunks: list[dict]) -> tuple[bool, str]:
    if not chunks:
        return False, "No context chunks retrieved from the vector database."
    
    RELEVANCE_SCORE_THRESHOLD = 0.6
    valid_chunks = [c for c in chunks if c.get("score", 0) >= RELEVANCE_SCORE_THRESHOLD]
    
    if not valid_chunks:
        return False, f"None of the retrieved chunks met the minimum relevance score of {RELEVANCE_SCORE_THRESHOLD}."
        
    return True, f"Found {len(valid_chunks)} relevant context chunks."