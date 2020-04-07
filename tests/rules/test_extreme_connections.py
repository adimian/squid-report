from squidreport.rules.extreme_connections import ExtremeConnectionsRule


def test_extreme_connections_rule_triggered(config_with_log_dir):
    rule = ExtremeConnectionsRule(
        config=config_with_log_dir("extreme_connections")
    )
    rule.evaluate()

    assert len(rule.messages) == 1
    assert "nb_positives=1" in rule.messages[0].context
