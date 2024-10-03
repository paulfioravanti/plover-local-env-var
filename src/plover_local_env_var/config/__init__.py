"""
# Config

A package dealing with:
    - loading and saving config containing env var names
"""

__all__ = [
    "CONFIG_BASENAME",
    "load",
    "save"
]

from .loader import (
    load,
    save
)


CONFIG_BASENAME: str = "local_env_var.json"
