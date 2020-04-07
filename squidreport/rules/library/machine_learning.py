import numpy as np
import pandas as pd
from sklearn import preprocessing


def clean_data(data):
    # Select data
    selected_data = data[
        [
            "uid",
            "id_orig_h",
            "id_resp_h",
            "id_resp_p",
            "orig_pkts",
            "resp_pkts",
            "orig_bytes",
            "resp_bytes",
            "service",
            "proto",
            "duration",
            "ts",
            "conn_state",
        ]
    ].copy()

    # Select data without '-' or if there is SH connection state
    filtered_data = selected_data.loc[
        (selected_data["duration"] != "-")
        | (selected_data["conn_state"] == "SH")
    ].copy()

    # Replace data SH with '-' by 0 value
    data_without_proto = filtered_data.loc[
        :, filtered_data.columns != "proto"
    ].copy()
    data_without_proto.replace("-", 0, inplace=True)
    data_without_proto["proto"] = filtered_data["proto"]

    # Change type columns to int and float
    for col_name, type in [
        ("orig_bytes", int),
        ("resp_bytes", int),
        ("orig_pkts", int),
        ("resp_pkts", int),
        ("ts", float),
        ("duration", float),
    ]:
        data_without_proto[col_name] = data_without_proto[col_name].astype(
            type
        )
    return data_without_proto


def normalize_data(data):
    standard_scaler = preprocessing.StandardScaler()
    normalized_data = standard_scaler.fit_transform(data)
    normalized_data = pd.DataFrame(normalized_data)
    normalized_data.columns = data.columns
    return normalized_data


def select_numerical_data(data):
    numeric_col_names = [
        col_name
        for col_name in data.columns
        if np.issubdtype(data[col_name].dtype, np.number)
    ]
    return data[numeric_col_names].copy()


def delete_internal_connections(data, known_hosts):
    conn_file_log_value = data.loc[
        (data["id_orig_h"].isin(known_hosts))
        ^ (data["id_resp_h"].isin(known_hosts))
    ]
    return conn_file_log_value
