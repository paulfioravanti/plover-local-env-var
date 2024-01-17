"""
Env Var - a module for dealing with fetching local ENV var values.
"""
import os
import re


_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_DEFAULT_SHELL = "bash"
_VAR_DIVIDER = "##"

def expand(var: str) -> str:
    """
    Fetches and returns a single local env var value.

    Raises an error if `var` is not an ENV var or a value for the env var
    cannot be found.
    """
    if not re.match(_ENV_VAR, var):
        raise ValueError(f"Provided value not an $ENV_VAR: {var}")

    expanded = _perform_expansion(var)

    if not expanded:
        raise ValueError(f"No value found for env var: {var}")

    return expanded

def expand_list(var_name_list: list[str]) -> dict[str, str]:
    """
    Returns a dict of env var values from a list of env var names.

    Removes a var from the list if:
        - its name not an ENV var
        - its value is blank.
    """
    var_name_list = [
        var_name for var_name in var_name_list if re.match(_ENV_VAR, var_name)
    ]
    var_names = _VAR_DIVIDER.join(var_name_list)
    expanded = _perform_expansion(var_names)
    env_vars = dict(zip(var_name_list, expanded.split(_VAR_DIVIDER)))
    valid_env_vars = {key: value for (key, value) in env_vars.items() if value}

    return valid_env_vars

def _perform_expansion(target: str) -> str:
    shell = os.environ.get("SHELL", _DEFAULT_SHELL).split("/")[-1]
    # NOTE: Using an interactive mode command (bash/zsh/fish -ic) seemed to be
    # the only way to access a user's env vars on a Mac outside Plover's
    # environment.
    return os.popen(f"{shell} -ic 'echo {target}'").read().strip()
