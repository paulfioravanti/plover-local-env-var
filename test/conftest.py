import pytest


@pytest.fixture()
def bash_command():
    return lambda env_var: f"bash -ic 'echo {env_var}'"

@pytest.fixture()
def powershell_command():
    return lambda env_var: (
        f"echo $ExecutionContext.InvokeCommand.ExpandString({env_var})"
    )
