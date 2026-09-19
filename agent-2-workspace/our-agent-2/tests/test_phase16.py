import pytest

from app.knowledge.health import (
    ComponentHealth,
    KnowledgeHealthChecker,
    KnowledgeSystemHealth,
)


def test_component_health_creation():
    component = ComponentHealth(
        name="retrieval",
        healthy=True,
        message="OK",
    )

    assert component.name == "retrieval"
    assert component.healthy
    assert component.message == "OK"


def test_healthy_system():
    health = KnowledgeSystemHealth(
        healthy=True,
        components=[
            ComponentHealth("retrieval", True),
            ComponentHealth("cache", True),
        ],
    )

    assert health.healthy
    assert health.unhealthy_components == []


def test_unhealthy_components_are_reported():
    health = KnowledgeSystemHealth(
        healthy=False,
        components=[
            ComponentHealth("retrieval", True),
            ComponentHealth("llm", False, "provider unavailable"),
        ],
    )

    assert health.unhealthy_components == ["llm"]


def test_health_summary():
    health = KnowledgeSystemHealth(
        healthy=True,
        components=[
            ComponentHealth("retrieval", True, "ready"),
        ],
    )

    summary = health.summary()

    assert summary["healthy"] is True
    assert summary["components"]["retrieval"]["healthy"] is True
    assert summary["unhealthy_components"] == []


def test_checker_runs_registered_checks():
    checker = KnowledgeHealthChecker()

    checker.register_check(
        "retrieval",
        lambda: (True, "ready"),
    )

    checker.register_check(
        "cache",
        lambda: True,
    )

    result = checker.check()

    assert result.healthy
    assert len(result.components) == 2


def test_checker_detects_failed_check():
    checker = KnowledgeHealthChecker()

    checker.register_check(
        "retrieval",
        lambda: (False, "index unavailable"),
    )

    result = checker.check()

    assert not result.healthy
    assert result.unhealthy_components == ["retrieval"]
    assert result.components[0].message == "index unavailable"


def test_checker_handles_exceptions():
    checker = KnowledgeHealthChecker()

    def broken_check():
        raise RuntimeError("database unavailable")

    checker.register_check("database", broken_check)

    result = checker.check()

    assert not result.healthy
    assert result.unhealthy_components == ["database"]
    assert "database unavailable" in result.components[0].message


def test_checker_rejects_empty_name():
    checker = KnowledgeHealthChecker()

    with pytest.raises(ValueError):
        checker.register_check("", lambda: True)


def test_checker_without_checks_is_healthy():
    checker = KnowledgeHealthChecker()

    result = checker.check()

    assert result.healthy
    assert result.components == []
