from abc import ABC, abstractmethod
import re


class LLMClient(ABC):

    @abstractmethod
    def generate(self, system_prompt, user_prompt):
        raise NotImplementedError


class MockLLMClient(LLMClient):

    def generate(self, system_prompt, user_prompt):
        evidence_ids = re.findall(
            r"EVIDENCE ID:\s*\[(E\d+)\]",
            user_prompt,
        )

        citations = " ".join(
            f"[{evidence_id}]"
            for evidence_id in evidence_ids[:3]
        )

        return (
            "Mock LLM response. "
            "The retrieval and context pipeline is working. "
            f"{citations}"
        )