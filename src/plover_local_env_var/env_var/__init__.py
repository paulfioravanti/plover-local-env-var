"""
# Env Var

A package dealing with:
    - expanding local environment variables and returning their values
"""

__all__ = [
    "expand",
    "expand_list",
    "resolve_command"
]

from .command import (
    resolve_command
)
from .expander import (
    expand,
    expand_list
)
