"""
Module to handle reading in the application JSON config file.
"""
from pathlib import Path
from typing import (
    Any,
    Callable
)

from .. import env_var
from . import (
    file,
    transformer
)


def load(
    shell_command: Callable[[str], str],
    config_filepath: Path
) -> dict[str, str]:
    """
    Reads in the config JSON file and expands each variable.

    Raises an error if the specified config file is not JSON format.
    """
    data: dict[str, Any] = file.load(config_filepath) # extractor function
    env_var_names: list[str] = transformer.transform_inbound(data)

    if not env_var_names:
        return {}

    env_vars: dict[str, str] = env_var.expand_list(shell_command, env_var_names)
    _save_any_changes(config_filepath, env_var_names, env_vars)

    return env_vars

def save(config_filepath: Path, env_var_names: list[str]) -> None:
    """
    Saves the set of env var names to the config JSON file.
    """
    data: dict[str, list[str]] = transformer.transform_outbound(env_var_names)
    file.save(config_filepath, data)

def _save_any_changes(
    config_filepath: Path,
    env_var_names: list[str],
    env_vars: dict[str, str]
) -> None:
    sorted_env_var_names: list[str] = sorted(env_vars.keys())

    if sorted_env_var_names != env_var_names:
        save(config_filepath, sorted_env_var_names)
