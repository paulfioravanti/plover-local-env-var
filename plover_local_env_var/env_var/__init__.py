"""
# Env Var

A package dealing with:
    - expanding local environment variables and returning their values
"""
from .command import (
    resolve_command
)
from .expander import (
    expand,
    expand_list
)

__all__ = [
    "expand",
    "expand_list",
    "resolve_command"
]
