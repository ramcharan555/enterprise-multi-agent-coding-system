from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentContext:
    query: str
    code_results: List[Any] = field(default_factory=list)
    knowledge_results: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def combined_results(self) -> List[Any]:
        return [*self.code_results, *self.knowledge_results]
