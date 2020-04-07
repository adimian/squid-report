import os
import pandas as pd

import joblib

from . import BaseRule
from .library.machine_learning import (
    clean_data,
    delete_internal_connections,
    select_numerical_data,
)
from .library.read_log_file import get_conn_file, get_known_hosts_file


def compute_data_for_beaconing_analysis(data):
    data_computed = pd.DataFrame()
    # For each connection on the same (origin, response:port)
    for (origin, response, port), data_for_group in data.groupby(
        ["id_orig_h", "id_resp_h", "id_resp_p"]
    ):
        # Analyse only connections that appear +2 times
        if len(data_for_group.index) >= 2:
            computed_data = {
                "std_" + k: data_for_group.loc[:, k].std()
                for k in [
                    "orig_bytes",
                    "resp_bytes",
                    "orig_pkts",
                    "resp_pkts",
                    "duration",
                ]
            }
            diff_ts = pd.Series(
                [
                    data_for_group.iloc[i + 1]["ts"]
                    - data_for_group.iloc[i]["ts"]
                    for i in range(len(data_for_group.index) - 1)
                ],
                dtype=float,
            )
            computed_data.update(
                {
                    "mean_diff_ts": diff_ts.mean(),
                    "id_orig_h": origin,
                    "id_resp_h": response,
                    "id_resp_p": port,
                }
            )
            data_computed = data_computed.append(
                computed_data, ignore_index=True
            )
    return data_computed


class Beaconing(BaseRule):
    @property
    def code(self):
        return "BEACONING"

    def evaluate(self):
        # Prepare data
        df = get_conn_file(self.config)
        known_host = get_known_hosts_file(self.config)

        cleaned_data = clean_data(df)

        data_without_internal_co = delete_internal_connections(
            cleaned_data, list(known_host["host"])
        )

        data_for_beaconing = compute_data_for_beaconing_analysis(
            data_without_internal_co
        )

        data_for_beaconing.pop("id_resp_p")
        X = select_numerical_data(data_for_beaconing)

        # Apply PCA
        pca = joblib.load(
            os.path.join(self.config.MODELS_DIRECTORY, "pca_beaconing.model")
        )
        X_pca = pca.transform(X)

        # Load model
        model = joblib.load(
            os.path.join(self.config.MODELS_DIRECTORY, "beaconing.model")
        )

        # Predict
        y_pred = model.predict(X_pca)

        nb_positives = sum(y_pred)
        if nb_positives:
            self.alert(nb_positives=nb_positives)
