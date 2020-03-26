import pytest

from squidreport.report import generate_messages
from squidreport.rules import BaseRule, Message


@pytest.fixture
def silent_rule():
    class SilentRule(BaseRule):
        @property
        def code(self):
            return "SILENT"

        def evaluate(self):
            return []

    return SilentRule


@pytest.fixture
def verbose_rule():
    class VerboseRule(BaseRule):
        @property
        def code(self):
            return "VERBOSE"

        def evaluate(self):
            return [Message(code=self.code)]

    return VerboseRule


def test_generate_messages(rule_config, silent_rule, verbose_rule):
    messages = generate_messages(
        rule_config, rules=[silent_rule, verbose_rule]
    )
    assert messages
    assert all(isinstance(m, Message) for m in messages)
    assert all(m.code == "VERBOSE" for m in messages)
