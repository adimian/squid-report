import pandas

from squidreport.rules.library.machine_learning import (
    clean_data,
    normalize_data,
    select_numerical_data,
)


def test_clean_data():
    data = pandas.DataFrame(
        {
            "id_orig_h": [1, 2, 3, 4],
            "id_resp_h": [1, 2, 3, 4],
            "id_resp_p": [443, 443, 443, 443],
            "proto": ["-", "-", "-", "-"],
            "service": ["http", "http", "http", "http"],
            "uid": [1, 2, 3, 4],
            "orig_pkts": ["-", "-", "3", "4"],
            "resp_pkts": ["-", "-", "3", "4"],
            "orig_bytes": ["-", "-", "3", "4"],
            "resp_bytes": ["-", "-", "3", "4"],
            "duration": ["-", "-", "3", "4"],
            "ts": ["3", "6", "3", "4"],
            "conn_state": ["S0", "SH", "SH", "S0"],
            "USELESS_COL": ["These", "will", "be", "deleted."],
        }
    )

    cleaned_data = clean_data(data)

    assert cleaned_data.to_dict("list") == {
        "conn_state": ["SH", "SH", "S0"],
        "duration": [0.0, 3.0, 4.0],
        "id_orig_h": [2, 3, 4],
        "id_resp_h": [2, 3, 4],
        "id_resp_p": [443, 443, 443],
        "orig_bytes": [0, 3, 4],
        "orig_pkts": [0, 3, 4],
        "proto": ["-", "-", "-"],
        "resp_bytes": [0, 3, 4],
        "resp_pkts": [0, 3, 4],
        "service": ["http", "http", "http"],
        "ts": [6.0, 3.0, 4.0],
        "uid": [2, 3, 4],
    }


def test_normalize_data():
    data = pandas.DataFrame({"orig_bytes": [1, 1], "resp_bytes": [-0.5, 0.5]})
    normalized_data = normalize_data(data)

    assert normalized_data.to_dict("list") == {
        "orig_bytes": [0.0, 0.0],
        "resp_bytes": [-1.0, 1.0],
    }


def test_it_select_numerical_data():
    d = pandas.DataFrame(
        {
            "A": [True, False, True],
            "B": [4, 5, 6],
            "C": [7.0, 8.0, 9.8],
            "D": [1e19, 1e3, 1e78],
            "E": ["Yes", "I don't know", "Not really"],
        }
    )

    numerical_data = select_numerical_data(d)

    assert sorted(list(numerical_data.columns)) == ["B", "C", "D"]
