from squidreport import read_config


def test_config_can_be_read_from_file(sample_config_file):
    config = read_config(sample_config_file)
    assert config.SQUID_API_DSN == "http://user:password@localhost:8070/"
    assert config.ZEEK_LOGS_DIRECTORY == "tests/data/logs"
    assert config.DISABLE_RULES == {"BEACON", "TOPDNS", "WHOIS"}


def test_config_can_also_come_from_command_line_options(sample_config_file):
    config = read_config(sample_config_file, DISABLE_RULES=["A", "B", "C"])
    assert config.DISABLE_RULES == {"BEACON", "TOPDNS", "WHOIS", "A", "B", "C"}


def test_config_can_also_come_from_command_line_options_except_if_empty(
    sample_config_file,
):
    config = read_config(sample_config_file, DISABLE_RULES=[])
    assert config.DISABLE_RULES == {"BEACON", "TOPDNS", "WHOIS"}
