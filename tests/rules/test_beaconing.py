from statistics import stdev

import pandas as pd
from pytest import approx

from squidreport.rules.beaconing import (
    Beaconing,
    compute_data_for_beaconing_analysis,
)


def test_it_computes_data_for_beaconing_analysis():
    data = pd.DataFrame(
        {
            "id_orig_h": ["1", "2", "1", "2", "2"],
            "id_resp_h": ["A", "B", "A", "B", "B"],
            "id_resp_p": [10, 20, 10, 30, 20],
            "proto": ["http", "dns", "http", "https", "dns"],
            "service": ["-", "-", "-", "-", "-"],
            "conn_state": ["REJ", "S1", "S0", "OTH", "SH"],
            "orig_bytes": [10, 20, 5, 30, 20],
            "resp_bytes": [10, 20, 5, 30, 20],
            "orig_pkts": [10, 20, 5, 30, 20],
            "resp_pkts": [10, 20, 5, 30, 20],
            "ts": [1, 2, 3, 4, 5],
            "duration": [10, 20, 5, 30, 20],
        }
    )

    diff = compute_data_for_beaconing_analysis(data)

    std = stdev([10, 5])
    assert diff.to_dict("list") == {
        "id_orig_h": ["1", "2"],
        "id_resp_h": ["A", "B"],
        "id_resp_p": [10, 20],
        "mean_diff_ts": [2.0, 3.0],
        "std_duration": approx([std, 0.0]),
        "std_orig_bytes": approx([std, 0.0]),
        "std_orig_pkts": approx([std, 0.0]),
        "std_resp_bytes": approx([std, 0.0]),
        "std_resp_pkts": approx([std, 0.0]),
    }


def test_beaconing_rule_triggered(config_with_log_dir):
    rule = Beaconing(config=config_with_log_dir("beaconing"))
    rule.evaluate()

    assert rule.messages
