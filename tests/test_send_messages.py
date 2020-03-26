from squidreport.rules import Message
from squidreport.report import send_messages
from unittest import mock


def test_message_is_sent(rule_config):
    with mock.patch("requests.post") as post:
        messages = [Message(code="TEST", context="")]
        assert send_messages(config=rule_config, messages=messages) == 1
        post.assert_called()
        assert post.call_args.kwargs["json"]["code"] == "TEST"
