"""
Expander - a module for dealing with fetching and expanding local ENV var
values.
"""
import os
import re
from typing import (
    Callable,
    Optional,
    Pattern
)


_ENV_VAR: Pattern[str] = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_VAR_DIVIDER: str = "##"

def expand(shell_command: Callable[[str], str], var: str) -> str:
    """
    Fetches and returns a single local env var value.

    Raises an error if `var` is not an ENV var or a value for the env var
    cannot be found.
    """
    if not re.match(_ENV_VAR, var):
        raise ValueError(f"Provided value not an $ENV_VAR: {var}")

    expanded: str = _perform_expansion(shell_command, var)

    return expanded

def expand_list(
    shell_command: Callable[[str], str],
    env_var_name_list: list[str]
) -> dict[str, str]:
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
    expanded: str = _perform_expansion(shell_command, var_names)
    env_vars: dict[str, str] = dict(
        zip(parsed_env_var_name_list, expanded.split(_VAR_DIVIDER))
    )

    return {
        key: value
        for (key, value) in env_vars.items()
        if value
    }

def _perform_expansion(shell_command: Callable[[str], str], target: str) -> str:
    command: str = shell_command(target)
    expanded: Optional[str] = os.popen(command).read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {target}")

    return expanded
