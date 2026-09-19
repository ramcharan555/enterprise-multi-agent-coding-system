from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """Interface for embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        raise NotImplementedError

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed(text) for text in texts]


class HashEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic lightweight embedding provider for development/testing.

    This is NOT intended for production semantic retrieval.
    """

    def __init__(self, dimensions: int = 128) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")

        self.dimensions = dimensions

    def embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions

        for index, character in enumerate(text):
            position = (
                ord(character) + index
            ) % self.dimensions

            vector[position] += 1.0

        magnitude = sum(value * value for value in vector) ** 0.5

        if magnitude == 0:
            return vector

        return [
            value / magnitude
            for value in vector
        ]