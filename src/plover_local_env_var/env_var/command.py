"""
Command - a module for resolving the platform-appropriate command to fetch
environment variables.
"""

import os
import platform
import subprocess
from typing import Callable


_POWERSHELL_COMMAND: Callable[[str], list[str]] = lambda env_var: (
    [
        "powershell",
        "-command",
        f"$ExecutionContext.InvokeCommand.ExpandString(\"{env_var}\")"
    ]
)
# NOTE: Using an interactive mode command (bash/zsh/fish -ic) seemed to be
# the only way to access a user's env vars on a Mac outside Plover's
# environment.
_SHELL_COMMAND: Callable[[str], Callable[[str], list[str]]] = lambda shell: (
    lambda env_var: [f"{shell}", "-ic", f"echo {env_var}"]
)
_DEFAULT_SHELL: str = "bash"

def resolve_command() -> Callable[[str], list[str]]:
    """
    Resolves a shell command for a given platform.
    """
    if platform.system() == "Windows":
        return _POWERSHELL_COMMAND

    return _SHELL_COMMAND(
        os.getenv("SHELL", _DEFAULT_SHELL).split("/")[-1]
    )

def run_command(
    shell_command_resolver: Callable[[str], list[str]],
    target: str
) -> str:
    """
    Runs a provided shell command against target in a subprocess.
    """
    command: list[str] = shell_command_resolver(target)
    result: str = subprocess.run(
        command,
        capture_output=True,
        check=False,
        encoding="utf-8"
    ).stdout.strip()

    return result
