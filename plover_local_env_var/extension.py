"""
Plover entry point extension module for Plover Local Env Var.

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/meta.html
"""
import os
from pathlib import Path
import platform
from typing import Callable

from plover.engine import StenoEngine
from plover.formatting import (
    _Action,
    _Context
)
from plover.machine.base import STATE_RUNNING
from plover.oslayer.config import CONFIG_DIR
from plover.registry import registry

from . import (
    config,
    env_var
)


_CONFIG_FILEPATH: Path = Path(CONFIG_DIR) / "local_env_var.json"
_DEFAULT_SHELL: str = "bash"
_POWERSHELL_COMMAND: Callable[[str], str] = lambda env_var: (
    f"echo $ExecutionContext.InvokeCommand.ExpandString({env_var})"
)
# NOTE: Using an interactive mode command (bash/zsh/fish -ic) seemed to be
# the only way to access a user's env vars on a Mac outside Plover's
# environment.
_SHELL_COMMAND: Callable[[str], Callable[[str], str]] = lambda shell: (
    lambda env_var: f"{shell} -ic 'echo {env_var}'"
)

class LocalEnvVar:
    """
    Extension class that also registers a meta plugin.
    The meta deals with fetching local env var values.
    """
    _engine: StenoEngine
    _env_var_values: dict[str, str]
    _shell_command: Callable[[str], str]

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine

    def start(self) -> None:
        """
        Sets up the meta plugin and steno engine hooks
        """
        self._shell_command = LocalEnvVar._determine_platform_command()
        self._env_var_values = config.load(
            self._shell_command,
            _CONFIG_FILEPATH
        )
        registry.register_plugin("meta", "ENV_VAR", self._env_var)
        self._engine.hook_connect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def stop(self) -> None:
        """
        Tears down the steno engine hooks
        """
        self._engine.hook_disconnect(
            "machine_state_changed",
            self._machine_state_changed
        )

    @staticmethod
    def _determine_platform_command() -> Callable[[str], str]:
        if platform.system() == "Windows":
            return _POWERSHELL_COMMAND

        return _SHELL_COMMAND(
            os.getenv("SHELL", _DEFAULT_SHELL).split("/")[-1]
        )

    def _env_var(self, ctx: _Context, argument: str) -> _Action:
        """
        Fetches a local env var and stores it in memory for faster
        execution on subsequent calls.
        """
        if not argument:
            raise ValueError("No $ENV_VAR provided")

        env_var_value: str
        try:
            env_var_value = self._env_var_values[argument]
        except KeyError:
            env_var_value = env_var.expand(
                self._shell_command,
                argument
            )
            self._env_var_values[argument] = env_var_value
            config.save(
                _CONFIG_FILEPATH,
                sorted(self._env_var_values.keys())
            )

        action: _Action = ctx.new_action()
        action.text = env_var_value
        return action

    def _machine_state_changed(
        self,
        _machine_type: str,
        machine_state: str
    ) -> None:
        """
        This hook will be called when when the Plover UI "Reconnect" button is
        pressed. Resetting the `_env_var_values` dictionary allows for changes
        made to env vars to be re-read in.
        """
        if machine_state == STATE_RUNNING:
            self._env_var_values = config.load(
                self._shell_command,
                _CONFIG_FILEPATH
            )
