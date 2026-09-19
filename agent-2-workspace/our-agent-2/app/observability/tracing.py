from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class TraceSpan:
    name: str
    started_at: datetime
    duration_ms: float
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "success"


@dataclass
class RequestTrace:
    trace_id: str
    request_name: str
    started_at: datetime
    spans: List[TraceSpan] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "success"

    @classmethod
    def create(
        cls,
        request_name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> "RequestTrace":
        return cls(
            trace_id=str(uuid.uuid4()),
            request_name=request_name,
            started_at=datetime.now(timezone.utc),
            attributes=attributes or {},
        )

    def add_span(
        self,
        name: str,
        duration_ms: float,
        attributes: Optional[Dict[str, Any]] = None,
        status: str = "success",
    ) -> TraceSpan:
        span = TraceSpan(
            name=name,
            started_at=datetime.now(timezone.utc),
            duration_ms=duration_ms,
            attributes=attributes or {},
            status=status,
        )
        self.spans.append(span)
        if status != "success":
            self.status = "failure"
        return span

    def summary(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "request_name": self.request_name,
            "started_at": self.started_at.isoformat(),
            "status": self.status,
            "span_count": len(self.spans),
            "total_duration_ms": sum(span.duration_ms for span in self.spans),
            "attributes": dict(self.attributes),
        }


class TraceCollector:
    def __init__(self) -> None:
        self._traces: List[RequestTrace] = []

    def start(
        self,
        request_name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> RequestTrace:
        trace = RequestTrace.create(request_name, attributes)
        self._traces.append(trace)
        return trace

    def record_span(
        self,
        trace: RequestTrace,
        name: str,
        operation,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        started = time.perf_counter()
        try:
            result = operation()
            duration_ms = (time.perf_counter() - started) * 1000
            trace.add_span(name, duration_ms, attributes, "success")
            return result
        except Exception:
            duration_ms = (time.perf_counter() - started) * 1000
            trace.add_span(name, duration_ms, attributes, "failure")
            trace.status = "failure"
            raise

    def traces(self) -> List[RequestTrace]:
        return list(self._traces)

    def clear(self) -> None:
        self._traces.clear()

    def summary(self) -> Dict[str, Any]:
        return {
            "trace_count": len(self._traces),
            "successful_traces": sum(
                trace.status == "success" for trace in self._traces
            ),
            "failed_traces": sum(
                trace.status == "failure" for trace in self._traces
            ),
        }
