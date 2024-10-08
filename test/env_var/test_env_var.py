import os
import pytest
import subprocess

from plover_local_env_var import env_var


def test_resolve_shell_command_for_windows(monkeypatch, powershell_command):
    monkeypatch.setattr("platform.system", lambda: "Windows")

    # REF: https://stackoverflow.com/a/20059029/567863
    assert (
        env_var.resolve_command().__code__.co_code
        == powershell_command.__code__.co_code
    )

def test_resolve_shell_command_for_mac_or_linux(monkeypatch, shell_command):
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(os, "getenv", lambda _shell, _default_shell: "bash")

    # REF: https://stackoverflow.com/a/20059029/567863
    assert (
        env_var.resolve_command().__code__.co_code
        == shell_command("bash").__code__.co_code
    )

def test_var_not_a_dollar_env_var(bash_command):
    with pytest.raises(
        ValueError,
        match="Provided value not an \\$ENV_VAR: FOO"
    ):
        env_var.expand(bash_command, "FOO")

def test_no_value_for_var_found_on_mac_on_linux(
    mock_subprocess_run,
    mocker,
    bash_command
):
    mock_subprocess_run(return_value="")
    spy = mocker.spy(subprocess, "run")

    with pytest.raises(ValueError, match="No value found for env var: \\$FOO"):
        env_var.expand(bash_command, "$FOO")

    spy.assert_called_once_with(
        ["bash", "-ic", "echo $FOO"],
        capture_output=True,
        check=False,
        encoding="utf-8"
    )

def test_no_value_for_var_found_on_windows(
    mock_subprocess_run,
    mocker,
    powershell_command
):
    mock_subprocess_run(return_value="")
    spy = mocker.spy(subprocess, "run")

    with pytest.raises(
        ValueError,
        match="No value found for env var: \\$ENV:FOO"
    ):
        env_var.expand(powershell_command, "$ENV:FOO")

    spy.assert_called_once_with(
        [
            "powershell",
            "-command",
            "$ExecutionContext.InvokeCommand.ExpandString(\"$ENV:FOO\")"
        ],
        capture_output=True,
        check=False,
        encoding="utf-8"
    )

def test_returns_expanded_value_of_found_env_var_on_mac_or_linux(
    mock_subprocess_run,
    mocker,
    bash_command
):
    mock_subprocess_run(return_value="Bar")
    spy = mocker.spy(subprocess, "run")

    assert env_var.expand(bash_command, "$FOO") == "Bar"
    spy.assert_called_once_with(
        ["bash", "-ic", "echo $FOO"],
        capture_output=True,
        check=False,
        encoding="utf-8"
    )

def test_returns_expanded_value_of_found_env_var_on_windows(
    mock_subprocess_run,
    mocker,
    powershell_command
):
    mock_subprocess_run(return_value="Bar")
    spy = mocker.spy(subprocess, "run")

    assert env_var.expand(powershell_command, "$ENV:FOO") == "Bar"
    spy.assert_called_once_with(
        [
            "powershell",
            "-command",
            "$ExecutionContext.InvokeCommand.ExpandString(\"$ENV:FOO\")"
        ],
        capture_output=True,
        check=False,
        encoding="utf-8"
    )
