import os
import pytest


@pytest.fixture
def current_test_dir():
    return os.path.dirname(__file__)


@pytest.fixture
def data_dir(current_test_dir):
    return os.path.join(current_test_dir, "data")


@pytest.fixture
def sample_config_file(data_dir):
    return os.path.join(data_dir, "sample-config.yml")
