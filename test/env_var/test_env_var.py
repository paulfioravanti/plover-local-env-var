import os
import pytest

from plover_local_env_var import env_var

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

def test_var_not_a_dollar_env_var(bash_command):
    with pytest.raises(
        ValueError,
        match="Provided value not an \\$ENV_VAR: FOO"
    ):
        env_var.expand(bash_command, "FOO")

def test_no_value_for_var_found_on_mac_on_linux(
    mock_popen_read,
    mocker,
    bash_command
):
    mock_popen_read(return_value="")
    spy = mocker.spy(os, "popen")

    with pytest.raises(ValueError, match="No value found for env var: \\$FOO"):
        env_var.expand(bash_command, "$FOO")

    spy.assert_called_once_with("bash -ic 'echo $FOO'")

def test_no_value_for_var_found_on_windows(
    mock_popen_read,
    mocker,
    powershell_command
):
    mock_popen_read(return_value="")
    spy = mocker.spy(os, "popen")

    with pytest.raises(
        ValueError,
        match="No value found for env var: \\$ENV:FOO"
    ):
        env_var.expand(powershell_command, "$ENV:FOO")

    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString($ENV:FOO)"
    )

def test_returns_expanded_value_of_found_env_var_on_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command
):
    mock_popen_read(return_value="Bar")
    spy = mocker.spy(os, "popen")

    assert env_var.expand(bash_command, "$FOO") == "Bar"
    spy.assert_called_once_with("bash -ic 'echo $FOO'")

def test_returns_expanded_value_of_found_env_var_on_windows(
    mock_popen_read,
    mocker,
    powershell_command
):
    mock_popen_read(return_value="Bar")
    spy = mocker.spy(os, "popen")

    assert env_var.expand(powershell_command, "$ENV:FOO") == "Bar"
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString($ENV:FOO)"
    )
