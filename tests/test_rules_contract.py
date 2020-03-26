import os

import pytest

from squidreport import Config
from squidreport.rules import BaseRule, Message


@pytest.fixture
def rule_config(data_dir):
    return Config(
        SQUID_API_DSN="", ZEEK_LOGS_DIRECTORY=os.path.join(data_dir, "logs")
    )


def test_rules_obey_contract(rule_config):
    class CustomRule(BaseRule):
        def evaluate(self):
            return [Message()]

    c = CustomRule(rule_config)
    messages = c.evaluate()

    assert messages
    assert all(isinstance(m, Message) for m in messages)
