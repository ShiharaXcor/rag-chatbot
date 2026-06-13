import  re    

# These block the document from being uploaded
SENSITIVE_PATTERNS = [
    r"password\s*[:=]\s*\S+",
    r"api[_\s]?key\s*[:=]\s*\S+",
    r"secret\s*[:=]\s*\S+",
    r"\b\d{3}-\d{2}-\d{4}\b",          # SSN format
    r"\b\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}\b",  # Credit card
]


# These block questions from being answered
BLOCKED_QUESTION_WORDS = [
    "porn", "explicit", "nude", "sex", "hack", "crack password",
    "bomb", "weapon", "drug synthesis", "illegal"
]

def is_document_safe(text: str) -> dict:
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "safe": False,
                "reason": "Document contains sensitive data (passwords, credentials, or PII). Please remove before uploading."
            }
    return {"safe": True, "reason": None}

def is_question_safe(question: str) -> dict:
    q_lower = question.lower()
    for word in BLOCKED_QUESTION_WORDS:
        if word in q_lower:
            return {
                "safe": False,
                "reason": "This question contains restricted content and cannot be processed."
            }
    if len(question.strip()) < 3:
        return {"safe": False, "reason": "Question is too short."}
    if len(question) > 1000:
        return {"safe": False, "reason": "Question is too long. Please shorten it."}
    return {"safe": True, "reason": None}
