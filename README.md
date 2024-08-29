# Plover Local Env Var

[![Build Status][Build Status image]][Build Status url] [![PyPI - Version][PyPI version image]][PyPI url] [![PyPI - Downloads][PyPI downloads image]][PyPI url] [![linting: pylint][linting image]][linting url]

This [Plover][] [extension][] [plugin][] contains a [meta][] that can read in
and output values stored in local [environment variables][] on your computer.

## Use Case

Ever have information that is not quite secret enough to warrant putting in a
password manager, but not public enough that you want to have steno dictionary
outlines containing it available to the public? Information like your phone
number, home address, and date of birth is very handy to have in outline values
when filling in online forms etc, but I wouldn't want to share that info in
[my steno dictionaries][].

So, in order to be able to share the outlines I use, but not the values
contained in them, I put that kind of semi-secret information in environment
variables, manage them with [direnv][], and use this plugin to access them in
order to write them out.

> [!NOTE]
> If you prefer to manually write out all your semi-secret information and/or
> you do not share your steno dictionaries publicly, you may not need to use
> this plugin at all.

> [!WARNING]
> Please do not put secret information like passwords in your steno dictionary
> outlines! Plover stands between when you write your keystrokes and when they
> output on screen, fitting the very definition of a ["man-in-the-middle"][]
> (see your `strokes.log` file for what Plover records by default). Use a
> password manager.

## Install

1. In the Plover application, open the Plugins Manager (either click the Plugins
   Manager icon, or from the `Tools` menu, select `Plugins Manager`).
2. From the list of plugins, find `plover-local-env-var`
3. Click "Install/Update"
4. When it finishes installing, restart Plover
5. After re-opening Plover, open the Configuration screen (either click the
   Configuration icon, or from the main Plover application menu, select
   `Preferences...`)
6. Open the Plugins tab
7. Check the box next to `plover_local_env_var` to activate the plugin

## How To Use

After defining and [exporting][] environment variables in your [shell
configuration file][], you can use them in your outlines with the `ENV_VAR`
meta. For an environment variable named `$PHONE_NUMBER`, the outline would look
like:

**macOS or Linux**

```json
"{:ENV_VAR:$PHONE_NUMBER}"
```

**Windows**

```json
"{:ENV_VAR:$ENV:PHONE_NUMBER}"
```

Pressing the "Disconnect and reconnect the machine" button on the Plover UI
resets the environment variable cache. If you make any changes to the values
contained in your environment variables, make sure to press it so they get
re-read in again.

All the fetched values also get cached, so subsequent calls to the same env var
get returned quicker.

## Development

Clone from GitHub with [git][]:

```console
git clone git@github.com:paulfioravanti/plover-local-env-var.git
cd plover-local-env-var
python -m pip install --editable ".[test]"
```

If you are a [Tmuxinator][] user, you may find my [plover_local_env_var project
file][] of reference.

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### Testing

- [Pytest][] is used for testing in this plugin.
- [Coverage.py][] and [pytest-cov][] are used for test coverage, and to run
  coverage within Pytest
- [Pylint][] is used for code quality
- [Mypy][] is used for static type checking

Currently, the only parts able to be tested are ones that do not rely directly
on Plover.

Run tests, coverage, and linting with the following commands:

```console
pytest --cov --cov-report=term-missing
pylint plover_local_env_var
mypy plover_local_env_var
```

To get a HTML test coverage report:

```console
coverage run --module pytest
coverage html
open htmlcov/index.html
```

If you are a [`just`][] user, you may find the [`justfile`][] useful during
development in running multiple test commands. You can run the following command
from the project root directory:

```console
just --working-directory . --justfile test/justfile
```

### Deploying Changes

After making any code changes, deploy the plugin into Plover with the following
command:

```console
plover --script plover_plugins install --editable .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

When necessary, the plugin can be uninstalled via the command line with the
following command:

```console
plover --script plover_plugins uninstall plover-local-env-var
```

[Build Status image]: https://github.com/paulfioravanti/plover-local-env-var/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-local-env-var/actions/workflows/ci.yml
[Coverage.py]: https://github.com/nedbat/coveragepy
[direnv]: https://direnv.net/
[environment variables]: https://en.wikipedia.org/wiki/Environment_variable
[exporting]: https://en.wikipedia.org/wiki/Environment_variable#Assignment:_Unix
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[`just`]: https://github.com/casey/just
[`justfile`]: ./test/justfile
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
["man-in-the-middle"]: https://en.wikipedia.org/wiki/Man-in-the-middle_attack
[meta]: https://plover.readthedocs.io/en/latest/plugin-dev/metas.html
[my steno dictionaries]: https://github.com/paulfioravanti/steno-dictionaries
[Mypy]: https://github.com/python/mypy
[Plover]: https://www.openstenoproject.org/
[plover_local_env_var project file]: https://github.com/paulfioravanti/dotfiles/blob/master/tmuxinator/plover_local_env_var.yml
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[PyPI downloads image]:https://img.shields.io/pypi/dm/plover-local-env-var
[PyPI version image]: https://img.shields.io/pypi/v/plover-local-env-var
[PyPI url]: https://pypi.org/project/plover-local-env-var/
[Pytest]: https://pytest.org/
[pytest-cov]: https://github.com/pytest-dev/pytest-cov/
[shell configuration file]: https://en.wikipedia.org/wiki/Unix_shell#Configuration_files
[Tmuxinator]: https://github.com/tmuxinator/tmuxinator
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
