from squidreport.rules.topdnsqueried import TopDNSQueriedRule


def test_top_dns_rule_triggered(config_with_log_dir):
    rule = TopDNSQueriedRule(config=config_with_log_dir("positives"))
    rule.evaluate()
    assert rule.messages
