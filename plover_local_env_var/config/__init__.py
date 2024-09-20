"""
# Config

A package dealing with:
    - loading and saving config containing env var names
"""
from .loader import (
    load,
    save
)

__all__ = [
    "CONFIG_BASENAME",
    "load",
    "save"
]

CONFIG_BASENAME: str = "local_env_var.json"
