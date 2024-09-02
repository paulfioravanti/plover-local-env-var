"""
# Config

A package dealing with:
    - loading and saving config containing env var names
"""
from .actions import (
    load,
    save
)
from .file import CONFIG_BASENAME

__all__ = [
    "CONFIG_BASENAME",
    "load",
    "save"
]
