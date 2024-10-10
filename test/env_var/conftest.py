import pytest


@pytest.fixture
def shell_command():
    def _method(shell):
        return lambda env_var: [f"{shell}", "-ic", f"echo {env_var}"]

    return _method
