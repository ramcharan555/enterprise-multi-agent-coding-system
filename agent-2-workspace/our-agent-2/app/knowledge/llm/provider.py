from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class LLMResponse:
    text: str
    model: str
    usage: dict


class LLMProvider(ABC):
    """Provider-independent interface for language models."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """Deterministic provider used for tests."""

    def __init__(self, model: str = "mock-llm"):
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        return LLMResponse(
            text="Generated answer from grounded evidence.",
            model=self.model,
            usage={
                "prompt_tokens": 0,
                "completion_tokens": 0,
            },
        )