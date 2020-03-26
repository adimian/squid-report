from abc import ABC, abstractmethod


class BaseRule(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def evaluate(self):
        pass


class Message:
    pass
