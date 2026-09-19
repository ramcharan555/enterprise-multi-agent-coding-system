from dataclasses import dataclass
from typing import List


@dataclass
class EvaluationCase:
    query: str
    expected_symbols: List[str]
    expected_files: List[str]
    expected_intent: str


_DATASET = [
    # ============================================================
    # SEND — EXPLANATION
    # ============================================================
    {
        "query": "How does send work?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain how a request is sent.",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What does the send function do?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What is the purpose of send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Describe the request sending flow.",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How is an HTTP request actually sent?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What happens when send is called?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain the behavior of send.",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How does the send method process a request?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What is send responsible for?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },

    # ============================================================
    # POST — EXPLANATION
    # ============================================================
    {
        "query": "What does post do?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What function performs the POST request?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain how post works.",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What is the purpose of the post function?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How is a POST request handled?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What happens when post is called?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Describe the post function.",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How does post process its request?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What is post responsible for?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain the behavior of post.",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },

    # ============================================================
    # SESSION — EXPLANATION
    # ============================================================
    {
        "query": "What is the purpose of Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain what Session does.",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How does the Session class work?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Describe the role of Session.",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What does the Session class handle?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What happens inside Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain the behavior of Session.",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What is Session responsible for?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How does a Session manage requests?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Describe how Session handles requests.",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },

    # ============================================================
    # LOCATION
    # ============================================================
    {
        "query": "Where is Session defined?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where is the Session class located?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where is post implemented?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where is send defined?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Which file contains the Session class?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Which file implements post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where can I find the implementation of send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Which file defines Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where can I find post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where can I find send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },

    # ============================================================
    # DEPENDENCY
    # ============================================================
    {
        "query": "What calls send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which code depends on send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Who calls the send function?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "What depends on Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which functions call Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "What code uses the Session class?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which code uses send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which functions depend on Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which functions call send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Who uses the Session class?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },

    # ============================================================
    # CROSS-FILE / NATURAL LANGUAGE
    # ============================================================
    {
        "query": "How does a request move through the code?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "How does the library send HTTP requests?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain the HTTP request flow.",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Which component sends an HTTP request?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Which component handles POST requests?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Which class manages HTTP sessions?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "Explain how HTTP sessions are managed.",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What part of the code sends requests?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What part of the code handles POST?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },
    {
        "query": "What code manages a Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "explanation",
    },

    # ============================================================
    # MORE LOCATION
    # ============================================================
    {
        "query": "What file is send in?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "What file contains send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where does the send implementation live?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where does the post implementation live?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "What file contains post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where does Session live?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Which source file defines Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Which source file contains send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Which source file contains post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },
    {
        "query": "Where is the implementation for Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "location",
    },

    # ============================================================
    # MORE DEPENDENCY
    # ============================================================
    {
        "query": "Which code calls send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which code calls post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Who uses send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Who uses post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "What depends on send?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "What depends on post?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which code depends on Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "Which functions use Session?",
        "expected_symbols": ["Session"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "What uses the send function?",
        "expected_symbols": ["send"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
    {
        "query": "What uses the post function?",
        "expected_symbols": ["post"],
        "expected_files": ["src/requests/sessions.py"],
        "expected_intent": "dependency",
    },
]


EVALUATION_DATASET = [
    EvaluationCase(**item)
    for item in _DATASET
]