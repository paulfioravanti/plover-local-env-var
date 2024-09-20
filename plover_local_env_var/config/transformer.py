"""
Transformer

Module to handle transforming information from the application JSON config file
into a form the application can work with.
"""
from typing import Any

def transform_inbound(data: dict[str, Any]) -> list[str]:
    """
    Transform inbound config data, providing defaults values where not provided.
    """
    env_var_names: list[str] = data.get("env_var_names", [])

    if (
        isinstance(env_var_names, list)
        and all(isinstance(env_var, str) for env_var in env_var_names)
    ):
        return env_var_names

    raise ValueError("'env_var_names' must be a list of strings.")

def transform_outbound(env_var_names: list[str]) -> dict[str, list[str]]:
    """
    Transform filepaths into outbound config data.
    """
    return {"env_var_names": env_var_names}
