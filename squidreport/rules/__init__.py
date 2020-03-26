from abc import ABC, abstractmethod
import arrow
import attr


class BaseRule(ABC):
    def __init__(self, config):
        self.config = config

    @property
    @abstractmethod
    def code(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass


@attr.s
class Message:
    code = attr.ib(type=str)
    timestamp = attr.ib(type=arrow.Arrow, factory=arrow.now)
