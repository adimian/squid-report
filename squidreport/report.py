import requests


def generate_messages(config, rules):
    messages = []
    for rule in rules:
        r = rule(config)
        r.evaluate()
        messages.extend(r.messages)

    return messages


def send_messages(config, messages):
    for message in messages:
        payload = {"code": message.code, "timestamp": message.timestamp}
        response = requests.post(config.SQUID_API_DSN, json=payload)
        if not response.ok:
            raise Exception(response.text)

    return len(messages)


def report(config):
    from .rules import ALL_RULES

    messages = generate_messages(config, rules=ALL_RULES)
    send_messages(config, messages=messages)
