from abc import ABC, abstractmethod


class BaseAgent(ABC):

    name = "base"

    def __init__(self, toolkit=None):
        self.toolkit = toolkit

    @abstractmethod
    def run(self, query, context=None):
        pass