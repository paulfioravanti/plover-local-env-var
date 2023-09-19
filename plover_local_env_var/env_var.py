"""
Env Var - a module for dealing with fetching local ENV var values.
"""
import os
import re

_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")

def expand_env_var(var: str) -> str:
    """
    Fetches and returns local env var values.

    Raises an error if `var` is not an ENV var or a value for the env var
    cannot be found.
    """
    if not re.match(_ENV_VAR, var):
        raise ValueError(f"Provided value not an $ENV_VAR: {var}")

    # NOTE: Using os.popen with an interactive mode bash command
    # (bash -ci) seemed to be the only way to access a user's env
    # vars on their Mac outside Plover's environment.
    expanded = os.popen(f"bash -ci 'echo {var}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {var}")

    return expanded
