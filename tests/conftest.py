import pytest
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
_config_path = f"{dir_path}/test_config.json"

@pytest.fixture(scope='module')
def config_path() -> str:
    return _config_path