from abc import ABC, abstractmethod
import arrow
import attr


class BaseRule(ABC):
    def __init__(self, config):
        self.config = config
        self.messages = []

    @property
    @abstractmethod
    def code(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    def alert(self, **kwargs):
        context = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        self.messages.append(Message(code=self.code, context=context))


@attr.s
class Message:
    code = attr.ib(type=str)
    context = attr.ib(type=str)
    timestamp = attr.ib(type=arrow.Arrow, factory=arrow.now)


# import all rules below this line
from .topdnsqueried import TopDNSQueriedRule


#  enable all rules here
ALL_RULES = (TopDNSQueriedRule,)
