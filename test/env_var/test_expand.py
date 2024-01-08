import pytest

from plover_local_env_var import env_var


def test_var_not_a_dollar_env_var():
    with pytest.raises(
        ValueError,
        match="Provided value not an \\$ENV_VAR: foo"
    ):
        env_var.expand("foo")

def test_no_value_for_var_found(monkeypatch):
    monkeypatch.setenv("FOO", "")

    with pytest.raises(ValueError, match="No value found for env var: \\$FOO"):
        env_var.expand("$FOO")

def test_returns_expanded_value_of_found_env_var(monkeypatch):
    monkeypatch.setenv("FOO", "Bar")

    assert env_var.expand("$FOO") == "Bar"
