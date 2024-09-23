import json
import os
import pytest

from plover_local_env_var import config


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

    assert loaded_config == {"$ENV:BAR": "baz", "$ENV:FOO": "quux"}
    spy.assert_called_once_with(
        "powershell -command "
        f"\"$ExecutionContext.InvokeCommand.ExpandString($ENV:BAR##$ENV:FOO)\""
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

    assert loaded_config == {"$BAR": "baz", "$FOO": "quux"}
    spy.assert_called_once_with("bash -ic 'echo $BAR##$FOO'")

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
        "powershell -command "
        f"\"$ExecutionContext.InvokeCommand.ExpandString($ENV:BAR##$ENV:FOO)\""
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
    spy.assert_called_once_with("bash -ic 'echo $BAR##$FOO'")

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

    assert loaded_config == {"$ENV:BAR": "baz"}
    spy.assert_called_once_with(
        "powershell -command "
        f"\"$ExecutionContext.InvokeCommand.ExpandString($ENV:BAR##$ENV:FOO)\""
    )

    # Original config file has had null variable BAR removed from it
    with valid_env_var_names_windows_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == ["$ENV:BAR"]

def test_expanding_some_existing_env_vars_on_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command,
    valid_env_var_names_mac_linux_config_path,
):
    mock_popen_read(return_value="##baz")
    spy = mocker.spy(os, "popen")
    loaded_config = config.load(
        bash_command,
        valid_env_var_names_mac_linux_config_path
    )

    assert loaded_config == {"$FOO": "baz"}
    spy.assert_called_once_with("bash -ic 'echo $BAR##$FOO'")

    # Original config file has had null variable BAR removed from it
    with valid_env_var_names_mac_linux_config_path.open(
        encoding="utf-8"
    ) as file:
        data = json.load(file)
        file.close()
    config_env_var_names = data.get("env_var_names", [])

    assert config_env_var_names == ["$FOO"]
