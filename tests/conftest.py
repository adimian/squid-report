import os
import pytest
from squidreport import Config


@pytest.fixture
def current_test_dir():
    return os.path.dirname(__file__)


@pytest.fixture
def data_dir(current_test_dir):
    return os.path.join(current_test_dir, "data")


@pytest.fixture
def sample_config_file(data_dir):
    return os.path.join(data_dir, "sample-config.yml")


@pytest.fixture
def rule_config(data_dir):
    return Config(
        SQUID_API_DSN="",
        ZEEK_LOGS_DIRECTORY=os.path.join(data_dir, "logs"),
        MODELS_DIRECTORY=os.path.join(data_dir, "model"),
    )


@pytest.fixture
def config_with_log_dir(data_dir):
    def config_factory(last_part):
        return Config(
            SQUID_API_DSN="",
            ZEEK_LOGS_DIRECTORY=os.path.join(data_dir, "logs", last_part),
            MODELS_DIRECTORY=os.path.join(data_dir, "model"),
        )

    return config_factory
