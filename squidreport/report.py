import requests


def generate_messages(config, rules):
    messages = []
    for rule in rules:
        r = rule(config)
        new_messages = r.evaluate()
        messages.extend(new_messages)

    return messages


def send_messages(config, messages):
    for message in messages:
        payload = {"code": message.code, "timestamp": message.timestamp}
        response = requests.post(config.SQUID_API_DSN, json=payload)
        if not response.ok:
            raise Exception(response.text)

    return len(messages)
