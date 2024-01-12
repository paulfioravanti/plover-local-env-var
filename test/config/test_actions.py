import json
from pathlib import Path
import pytest

from plover_local_env_var import config

# Files

@pytest.fixture
def bad_config_path():
    return (Path(__file__).parent / "files/bad_json_data.json").resolve()

@pytest.fixture
def non_existent_config_path():
    return (Path(__file__).parent / "files/non_existent.json").resolve()

@pytest.fixture
def non_array_env_var_names_config_path():
    return (
        (Path(__file__).parent / "files/non_array_env_var_names.json").resolve()
    )

@pytest.fixture
def valid_env_var_names_config_path():
    path = (Path(__file__).parent / "files/valid_env_var_names.json").resolve()
    with path.open(encoding="utf-8") as file:
        config_data = json.load(file)
        file.close()

    yield path

    with path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)
        file.close()

# Tests

def test_bad_config(bad_config_path):
    with pytest.raises(
        ValueError,
        match="Unable to decode file contents as JSON"
    ):
        config.load(bad_config_path)

def test_non_existent_config(non_existent_config_path):
    loaded_config = config.load(non_existent_config_path)
    assert loaded_config == {}

def test_config_with_non_array_env_var_names(
    non_array_env_var_names_config_path
):
    with pytest.raises(ValueError, match="'env_var_names' must be a list"):
        config.load(non_array_env_var_names_config_path)

def test_expanding_existing_env_vars(
    monkeypatch,
    valid_env_var_names_config_path
):
    monkeypatch.setenv("FOO", "baz")
    monkeypatch.setenv("BAR", "quux")
    loaded_config = config.load(valid_env_var_names_config_path)
    assert loaded_config == {"$FOO": "baz", "$BAR": "quux"}

    # No change to original config file
    with valid_env_var_names_config_path.open(encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])
    assert config_env_var_names == ["$BAR", "$FOO"]

def test_expanding_non_existent_env_vars(valid_env_var_names_config_path):
    loaded_config = config.load(valid_env_var_names_config_path)
    assert loaded_config == {}

    # Original config file has been blanked out
    with valid_env_var_names_config_path.open(encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])
    assert config_env_var_names == []

def test_expanding_some_existing_env_vars(
    monkeypatch,
    valid_env_var_names_config_path
):
    monkeypatch.setenv("FOO", "baz")
    monkeypatch.setenv("BAR", "")
    loaded_config = config.load(valid_env_var_names_config_path)
    assert loaded_config == {"$FOO": "baz"}

    # Original config file has had null variable BAR removed from it
    with valid_env_var_names_config_path.open(encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])
    assert config_env_var_names == ["$FOO"]
