from dataclasses import dataclass, field
from typing import Dict, List
import time


@dataclass
class ComponentHealth:
    name: str
    healthy: bool
    message: str = ""


@dataclass
class KnowledgeSystemHealth:
    healthy: bool
    components: List[ComponentHealth] = field(default_factory=list)
    checked_at: float = field(default_factory=time.time)

    @property
    def unhealthy_components(self) -> List[str]:
        return [
            component.name
            for component in self.components
            if not component.healthy
        ]

    def summary(self) -> Dict[str, object]:
        return {
            "healthy": self.healthy,
            "components": {
                component.name: {
                    "healthy": component.healthy,
                    "message": component.message,
                }
                for component in self.components
            },
            "unhealthy_components": self.unhealthy_components,
        }


class KnowledgeHealthChecker:
    def __init__(self):
        self._checks = {}

    def register_check(self, name, check):
        if not name.strip():
            raise ValueError("Health check name cannot be empty")
        self._checks[name] = check

    def check(self) -> KnowledgeSystemHealth:
        components = []

        for name, check in self._checks.items():
            try:
                result = check()

                if isinstance(result, tuple):
                    healthy, message = result
                else:
                    healthy, message = bool(result), ""

                components.append(
                    ComponentHealth(
                        name=name,
                        healthy=healthy,
                        message=str(message),
                    )
                )
            except Exception as exc:
                components.append(
                    ComponentHealth(
                        name=name,
                        healthy=False,
                        message=str(exc),
                    )
                )

        return KnowledgeSystemHealth(
            healthy=all(component.healthy for component in components),
            components=components,
        )
