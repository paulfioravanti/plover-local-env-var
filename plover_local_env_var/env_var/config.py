"""
Module to handle reading in the application JSON config file.
"""
import json
from pathlib import Path

from .expand import expand_list


def load(config_filepath: Path) -> dict[str, str]:
    """
    Reads in the config JSON file and expands each variable.

    Raises an error if the specified config file is not JSON format.
    """
    try:
        with config_filepath.open(encoding="utf-8") as file:
            data = json.load(file)
            file.close()
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError as exc:
        raise ValueError("Config file must contain a JSON object") from exc

    config_env_var_names = data.get("env_var_names", [])
    if not isinstance(config_env_var_names, list):
        raise ValueError("'env_var_names' must be a list")

    env_vars = expand_list(config_env_var_names)
    env_var_names = sorted(env_vars.keys())
    if env_var_names != config_env_var_names:
        save(config_filepath, env_var_names)

    return env_vars

def save(config_filepath: Path, env_var_names: dict[str, str]) -> None:
    """
    Saves the set of env var names to the config JSON file.
    """
    with config_filepath.open("w", encoding="utf-8") as file:
        json.dump({"env_var_names": env_var_names}, file)
        file.close()
