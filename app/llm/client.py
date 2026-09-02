from abc import ABC, abstractmethod


class LLMClient(ABC):

    @abstractmethod
    def generate(self, system_prompt, user_prompt):
        raise NotImplementedError


class MockLLMClient(LLMClient):

    def generate(self, system_prompt, user_prompt):
        return (
            "Mock LLM response. "
            "The retrieval and context pipeline is working."
        )