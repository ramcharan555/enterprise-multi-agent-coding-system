from app.query.router import QueryRouter


def test_location_query():
    router = QueryRouter()

    result = router.route(
        "Where is authentication implemented?"
    )

    assert result.intent == "location"
    assert result.confidence > 0.5


def test_explanation_query():
    router = QueryRouter()

    result = router.route(
        "How does HTTPAdapter send requests?"
    )

    assert result.intent == "explanation"


def test_dependency_query():
    router = QueryRouter()

    result = router.route(
        "Who are the callers of Session.send?"
    )

    assert result.intent == "dependency"


def test_debugging_query():
    router = QueryRouter()

    result = router.route(
        "Why does this test fail?"
    )

    assert result.intent == "debugging"


def test_coding_query():
    router = QueryRouter()

    result = router.route(
        "Add retry handling to HTTPAdapter"
    )

    assert result.intent == "coding"


def test_unknown_query():
    router = QueryRouter()

    result = router.route("")

    assert result.intent == "unknown"
    assert result.confidence == 0.0