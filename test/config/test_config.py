import json
import os
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
def valid_env_var_names_mac_linux_config_path():
    path = (
        Path(__file__).parent / "files/valid_env_var_names_mac_linux.json"
    ).resolve()
    with path.open(encoding="utf-8") as file:
        config_data = json.load(file)
        file.close()

    yield path

    with path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)
        file.close()

@pytest.fixture
def valid_env_var_names_windows_config_path():
    path = (
        Path(__file__).parent / "files/valid_env_var_names_windows.json"
    ).resolve()
    with path.open(encoding="utf-8") as file:
        config_data = json.load(file)
        file.close()

    yield path

    with path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)
        file.close()

# Other fixture types

# NOTE: Given that the command passed in to `os.popen` will be different
# between Windows and non-Windows:
#
# `echo $ExecutionContext.InvokeCommand.ExpandString($ENV:FOO)`
#
# vs
#
# `bash -ic 'echo $FOO'`
#
# This mock handwaves over how that command works, and what it returns, and
# instead just gives back a the `return_value` passed in that we're reasonably
# sure we're expecting back from `os.popen.read`.
@pytest.fixture()
def mock_popen_read(mocker):
    mock = mocker.Mock()
    mocker.patch("os.popen", return_value=mock)

    def _method(return_value=None):
        mock.read.return_value = return_value

    return _method

@pytest.fixture()
def bash_command():
    return lambda env_var: "bash -ic 'echo {0}'".format(env_var)

@pytest.fixture()
def powershell_command():
    return lambda env_var: (
        "echo $ExecutionContext.InvokeCommand.ExpandString({0})".format(env_var)
    )

# Tests

def test_bad_config(bad_config_path, bash_command):
    with pytest.raises(
        ValueError,
        match="Unable to decode file contents as JSON"
    ):
        config.load(bash_command, bad_config_path)

def test_non_existent_config(non_existent_config_path, bash_command):
    loaded_config = config.load(bash_command, non_existent_config_path)
    assert loaded_config == {}

def test_config_with_non_array_env_var_names(
    non_array_env_var_names_config_path,
    bash_command
):
    with pytest.raises(ValueError, match="'env_var_names' must be a list"):
        config.load(bash_command, non_array_env_var_names_config_path)

def test_expanding_existing_env_vars_on_windows(
    mock_popen_read,
    mocker,
    powershell_command,
    valid_env_var_names_windows_config_path
):
    mock_popen_read(return_value="baz##quux")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        powershell_command,
        valid_env_var_names_windows_config_path
    )

    assert loaded_config == {"$ENV:FOO": "baz", "$ENV:BAR": "quux"}
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString($ENV:FOO##$ENV:BAR)"
    )

    # No change to original config file
    with valid_env_var_names_windows_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == ["$ENV:BAR", "$ENV:FOO"]

def test_expanding_existing_env_vars_on_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command,
    valid_env_var_names_mac_linux_config_path,
):
    mock_popen_read(return_value="baz##quux")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        bash_command,
        valid_env_var_names_mac_linux_config_path
    )

    assert loaded_config == {"$FOO": "baz", "$BAR": "quux"}
    spy.assert_called_once_with("bash -ic 'echo $FOO##$BAR'")

    # No change to original config file
    with valid_env_var_names_mac_linux_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == ["$BAR", "$FOO"]

def test_expanding_non_existent_env_vars_on_windows(
    mock_popen_read,
    mocker,
    powershell_command,
    valid_env_var_names_windows_config_path,
):
    mock_popen_read(return_value="##")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        powershell_command,
        valid_env_var_names_windows_config_path
    )

    assert loaded_config == {}
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString($ENV:FOO##$ENV:BAR)"
    )

    # Original config file has been blanked out
    with valid_env_var_names_windows_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == []

def test_expanding_non_existent_env_vars_on_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command,
    valid_env_var_names_mac_linux_config_path,
):
    mock_popen_read(return_value="##")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        bash_command,
        valid_env_var_names_mac_linux_config_path
    )

    assert loaded_config == {}
    spy.assert_called_once_with("bash -ic 'echo $FOO##$BAR'")

    # Original config file has been blanked out
    with valid_env_var_names_mac_linux_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == []

def test_expanding_some_existing_env_vars_on_windows(
    mock_popen_read,
    mocker,
    powershell_command,
    valid_env_var_names_windows_config_path,
):
    mock_popen_read(return_value="baz##")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        powershell_command,
        valid_env_var_names_windows_config_path
    )

    assert loaded_config == {"$ENV:FOO": "baz"}
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString($ENV:FOO##$ENV:BAR)"
    )

    # Original config file has had null variable BAR removed from it
    with valid_env_var_names_windows_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == ["$ENV:FOO"]

def test_expanding_some_existing_env_vars_on_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command,
    valid_env_var_names_mac_linux_config_path,
):
    mock_popen_read(return_value="baz##")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        bash_command,
        valid_env_var_names_mac_linux_config_path
    )

    assert loaded_config == {"$FOO": "baz"}
    spy.assert_called_once_with("bash -ic 'echo $FOO##$BAR'")

    # Original config file has had null variable BAR removed from it
    with valid_env_var_names_mac_linux_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == ["$FOO"]
