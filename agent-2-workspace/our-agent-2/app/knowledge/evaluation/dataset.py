from app.knowledge.retrieval.evaluator import RetrievalEvaluationCase


DEFAULT_RETRIEVAL_DATASET = [
    RetrievalEvaluationCase(
        query="authentication implementation",
        relevant_document_ids=["auth.py"],
    ),
    RetrievalEvaluationCase(
        query="database connection",
        relevant_document_ids=["database.py"],
    ),
    RetrievalEvaluationCase(
        query="API configuration",
        relevant_document_ids=["api.py"],
    ),
    RetrievalEvaluationCase(
        query="authorization rules",
        relevant_document_ids=["auth.py", "security.py"],
    ),
]
