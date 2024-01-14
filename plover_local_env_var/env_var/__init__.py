"""
# Env Var

A package dealing with:
    - expanding local environment variables and returning their values
"""
from .expand import expand, expand_list

__all__ = [
    "expand",
    "expand_list"
]
