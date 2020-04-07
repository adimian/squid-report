from squidreport.rules.library.scraping import parse_wikipedia_port_proto
import pandas as pd


def test_if_data_wikipedia_isn_t_empty():
    assert parse_wikipedia_port_proto() is not None


def test_good_columns_name():
    columns_list = []
    for columns in parse_wikipedia_port_proto():
        columns_list.append(columns)
    expected_columns = ["Port", "TCP", "UDP", "IANA_status", "Description"]
    assert columns_list, expected_columns


def test_is_dataframe():
    port_info = parse_wikipedia_port_proto()
    assert isinstance(port_info, pd.DataFrame)
