"""
Expander - a module for dealing with fetching and expanding local ENV var
values.
"""
import os
import re
from typing import Pattern


_ENV_VAR: Pattern[str] = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_DEFAULT_SHELL: str = "bash"
_VAR_DIVIDER: str = "##"

def expand(var: str) -> str:
    """
    Fetches and returns a single local env var value.

    Raises an error if `var` is not an ENV var or a value for the env var
    cannot be found.
    """
    if not re.match(_ENV_VAR, var):
        raise ValueError(f"Provided value not an $ENV_VAR: {var}")

    expanded: str = _perform_expansion(var)

    if not expanded:
        raise ValueError(f"No value found for env var: {var}")

    return expanded

def expand_list(env_var_name_list: list[str]) -> dict[str, str]:
    """
    Returns a dict of env var values from a list of env var names.

    Removes a var from the list if:
        - its name not an ENV var
        - its value is blank.
    """
    parsed_env_var_name_list: list[str] = [
        var_name
        for var_name in env_var_name_list
        if re.match(_ENV_VAR, var_name)
    ]
    var_names: str = _VAR_DIVIDER.join(parsed_env_var_name_list)
    expanded: str = _perform_expansion(var_names)
    env_vars: dict[str, str] = dict(
        zip(parsed_env_var_name_list, expanded.split(_VAR_DIVIDER))
    )
    valid_env_vars: dict[str, str] = {
        key: value
        for (key, value) in env_vars.items()
        if value
    }

    return valid_env_vars

def _perform_expansion(target: str) -> str:
    # NOTE: Entire shell path cannot be used because Plover's shell location may
    # not be the same as the user's machine.
    shell: str = os.getenv("SHELL", _DEFAULT_SHELL).split("/")[-1]
    # NOTE: Using an interactive mode command (bash/zsh/fish -ic) seemed to be
    # the only way to access a user's env vars on a Mac outside Plover's
    # environment.
    return os.popen(f"{shell} -ic 'echo {target}'").read().strip()
