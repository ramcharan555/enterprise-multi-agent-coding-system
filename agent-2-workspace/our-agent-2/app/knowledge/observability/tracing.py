from dataclasses import dataclass, field
from typing import Dict, List
import time


@dataclass
class RetrievalTrace:
    query: str
    stages: List[str] = field(default_factory=list)
    metadata: Dict[str, object] = field(default_factory=dict)
    duration_ms: float = 0.0

    def add_stage(self, stage: str) -> None:
        self.stages.append(stage)

    def finish(self, started_at: float) -> None:
        self.duration_ms = (time.perf_counter() - started_at) * 1000


class RetrievalTracer:
    def start(self, query: str) -> RetrievalTrace:
        trace = RetrievalTrace(query=query)
        trace.add_stage("start")
        return trace

    def finish(self, trace: RetrievalTrace, started_at: float) -> RetrievalTrace:
        trace.add_stage("finish")
        trace.finish(started_at)
        return trace
