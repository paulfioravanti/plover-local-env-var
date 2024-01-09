"""
# Env Var

A package dealing with:
    - loading in local variable names from a config file
    - expanding local environment variables and returning their values
"""
from .expand import expand
from .config import load, save
