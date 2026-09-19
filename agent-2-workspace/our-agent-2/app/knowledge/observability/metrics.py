from dataclasses import dataclass, field
from typing import Dict


@dataclass
class RetrievalMetrics:
    queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    total_latency_ms: float = 0.0
    metadata: Dict[str, object] = field(default_factory=dict)

    @property
    def average_latency_ms(self) -> float:
        if self.queries == 0:
            return 0.0
        return self.total_latency_ms / self.queries

    def record_success(self, latency_ms: float) -> None:
        self.queries += 1
        self.successful_queries += 1
        self.total_latency_ms += latency_ms

    def record_failure(self, latency_ms: float) -> None:
        self.queries += 1
        self.failed_queries += 1
        self.total_latency_ms += latency_ms

    def snapshot(self) -> dict:
        return {
            "queries": self.queries,
            "successful_queries": self.successful_queries,
            "failed_queries": self.failed_queries,
            "average_latency_ms": self.average_latency_ms,
        }
