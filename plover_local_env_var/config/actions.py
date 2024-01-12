"""
Module to handle reading in the application JSON config file.
"""
from pathlib import Path
from typing import Any

from .. import env_var
from . import file


def load(config_filepath: Path) -> dict[str, str]:
    """
    Reads in the config JSON file and expands each variable.

    Raises an error if the specified config file is not JSON format.
    """
    data = file.load(config_filepath)
    config_env_var_names = _parse(data)
    if not config_env_var_names:
        return {}

    env_vars = env_var.expand_list(config_env_var_names)
    _save_any_changes(config_filepath, config_env_var_names, env_vars)
    return env_vars

def save(config_filepath: Path, env_var_names: list[str]) -> None:
    """
    Saves the set of env var names to the config JSON file.
    """
    data = {"env_var_names": env_var_names}
    file.save(config_filepath, data)

def _parse(data: dict[str, Any]) -> list[str]:
    env_var_names = data.get("env_var_names", [])

    if not isinstance(env_var_names, list):
        raise ValueError("'env_var_names' must be a list")

    return env_var_names

def _save_any_changes(
    config_filepath: Path,
    config_env_var_names: list[str],
    env_vars: dict[str, str]
) -> None:
    env_var_names = sorted(env_vars.keys())

    if env_var_names != config_env_var_names:
        save(config_filepath, env_var_names)
