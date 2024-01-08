"""
Env Var - a module for dealing with fetching local ENV var values.
"""
import os
import re


_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_DEFAULT_SHELL = "bash"
_INTERACTIVE_SHELLS = ["zsh", "bash"]

def expand(var: str) -> str:
    """
    Fetches and returns local env var values.

    Raises an error if `var` is not an ENV var or a value for the env var
    cannot be found.
    """
    if not re.match(_ENV_VAR, var):
        raise ValueError(f"Provided value not an $ENV_VAR: {var}")

    shell = os.environ.get("SHELL", _DEFAULT_SHELL).split("/")[-1]
    # NOTE: Using an interactive mode command (bash/zsh -ci) seemed to be the
    # only way to access a user's env vars on a Mac outside Plover's
    # environment.
    flags = "-ci" if shell in _INTERACTIVE_SHELLS else "-c"
    expanded = os.popen(f"{shell} {flags} 'echo {var}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {var}")

    return expanded
