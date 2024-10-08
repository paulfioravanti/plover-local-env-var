import json
from pathlib import Path
import pytest


@pytest.fixture
def bad_config_path():
    return _path("files/bad_json_data.json")

@pytest.fixture
def non_existent_config_path():
    return _path("files/non_existent.json")

@pytest.fixture
def non_array_env_var_names_config_path():
    return _path("files/non_array_env_var_names.json")

@pytest.fixture
def valid_env_var_names_mac_linux_config_path():
    path = _path("files/valid_env_var_names_mac_linux.json")
    with path.open(encoding="utf-8") as file:
        config_data = json.load(file)
        file.close()

    yield path

    with path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)
        file.close()

@pytest.fixture
def valid_env_var_names_windows_config_path():
    path = _path("files/valid_env_var_names_windows.json")
    with path.open(encoding="utf-8") as file:
        config_data = json.load(file)
        file.close()

    yield path

    with path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)
        file.close()

def _path(path):
    return (Path(__file__).parent / path).resolve()
