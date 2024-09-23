import pytest


@pytest.fixture
def bash_command():
    return lambda env_var: f"bash -ic 'echo {env_var}'"

@pytest.fixture
def powershell_command():
    return lambda env_var: (
        "powershell -command "
        f"\"$ExecutionContext.InvokeCommand.ExpandString({env_var})\""
    )

# NOTE: Given that the command passed in to `os.popen` will be different
# between Windows and non-Windows:
#
# `powershell -command "$ExecutionContext.InvokeCommand.ExpandString($ENV:FOO)"`
#
# vs
#
# `bash -ic 'echo $FOO'`
#
# This mock handwaves over how that command works, and what it returns, and
# instead just gives back a the `return_value` passed in that we're reasonably
# sure we're expecting back from `os.popen.read`.
@pytest.fixture
def mock_popen_read(mocker):
    mock = mocker.Mock()
    mocker.patch("os.popen", return_value=mock)

    def _method(return_value=None):
        mock.read.return_value = return_value

    return _method
