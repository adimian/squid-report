import os

import joblib

from . import BaseRule
from .library.machine_learning import (
    clean_data,
    normalize_data,
    select_numerical_data,
)
from .library.read_log_file import get_conn_file


class ExtremeConnectionsRule(BaseRule):
    @property
    def code(self):
        return "EXTREME_CONNECTIONS"

    def evaluate(self):
        # Prepare data
        df = get_conn_file(self.config)
        cleaned_data = clean_data(df)
        numerical_data = select_numerical_data(cleaned_data)
        numerical_data.pop("id_resp_p")
        X = normalize_data(numerical_data)

        # Load model
        model = joblib.load(
            os.path.join(
                self.config.MODELS_DIRECTORY, "extreme_connections.model"
            )
        )

        # Predict
        y_pred = model.predict(X)

        nb_positives = sum(y_pred)
        if nb_positives:
            self.alert(nb_positives=nb_positives)
