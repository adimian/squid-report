def generate_messages(config, rules):
    messages = []
    for rule in rules:
        r = rule(config)
        new_messages = r.evaluate()
        messages.extend(new_messages)

    return messages
