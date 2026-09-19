from app.knowledge.observability.metrics import RetrievalMetrics


def test_metrics_record_success():
    metrics = RetrievalMetrics()
    metrics.record_success(10.0)
    metrics.record_success(20.0)

    assert metrics.queries == 2
    assert metrics.successful_queries == 2
    assert metrics.failed_queries == 0
    assert metrics.average_latency_ms == 15.0


def test_metrics_record_failure():
    metrics = RetrievalMetrics()
    metrics.record_failure(30.0)

    assert metrics.queries == 1
    assert metrics.failed_queries == 1
    assert metrics.average_latency_ms == 30.0


def test_metrics_snapshot():
    metrics = RetrievalMetrics()
    metrics.record_success(5.0)

    snapshot = metrics.snapshot()

    assert snapshot["queries"] == 1
    assert snapshot["successful_queries"] == 1
    assert snapshot["average_latency_ms"] == 5.0
