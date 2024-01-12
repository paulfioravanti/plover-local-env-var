# Plover Local Env Var

[![Build Status][Build Status image]][Build Status url] [![linting: pylint][linting image]][linting url]

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

## Why a Plugin?

I used to access environment variables from a steno outline like in this
example:

```json
"PHAEUL/PHAEUL": "{:COMMAND:SHELL:bash -ci 'osascript $STENO_DICTIONARIES/src/command/actions/output-env-var.scpt EMAIL'}"
```

This solution does the following:

- uses the [Plover Run Shell][] plugin to run a shell command from Python
- calls `bash` in [interactive mode][] (`-i`) so that the command can see
  [environment variables][] (`$STENO_DICTIONARIES` in this case) defined outside
  of the Plover environment
- gets `bash` to use the [`osascript`][] command-line tool to load in and run
  the target compiled [AppleScript][] ([`.scpt`][]) file
- The AppleScript in question would then call out to the shell to fetch the
  `$EMAIL` env var, and keystroke it out to the screen

This stack of `Python->Shell->AppleScript->Shell` is convoluted and just not the
right tool for the job at hand. Plover Local Env Var just uses Python and Shell,
and reduces the outline above to be just:

```json
"PHAEUL/PHAEUL": "{:ENV_VAR:$EMAIL}"
```

All the fetched values also get cached, so subsequent calls to the same env var
get returned quicker.

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

```json
"{:ENV_VAR:$PHONE_NUMBER}"
```

Pressing the "Disconnect and reconnect the machine" button on the Plover UI
resets the environment variable cache. If you make any changes to the values
contained in your environment variables, make sure to press it so they get
re-read in again.

## Development

Clone from GitHub with [git][]:

```console
git clone git@github.com:paulfioravanti/plover-local-env-var.git
cd plover-local-env-var
```

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

### Deploying Changes

After making any code changes, deploy the plugin into Plover with the following
command:

```console
plover -s plover_plugins install .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

[AppleScript]: https://en.wikipedia.org/wiki/AppleScript
[Build Status image]: https://github.com/paulfioravanti/plover-local-env-var/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-local-env-var/actions/workflows/ci.yml
[Coverage.py]: https://github.com/nedbat/coveragepy
[direnv]: https://direnv.net/
[environment variables]: https://en.wikipedia.org/wiki/Environment_variable
[exporting]: https://en.wikipedia.org/wiki/Environment_variable#Assignment:_Unix
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[interactive mode]: https://www.gnu.org/software/bash/manual/html_node/Interactive-Shell-Behavior.html
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
["man-in-the-middle"]: https://en.wikipedia.org/wiki/Man-in-the-middle_attack
[meta]: https://plover.readthedocs.io/en/latest/plugin-dev/metas.html
[my steno dictionaries]: https://github.com/paulfioravanti/steno-dictionaries
[Mypy]: https://github.com/python/mypy
[`osascript`]: https://ss64.com/osx/osascript.html
[Plover]: https://www.openstenoproject.org/
[Plover Run Shell]: https://github.com/user202729/plover_run_shell
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[Pytest]: https://pytest.org/
[pytest-cov]: https://github.com/pytest-dev/pytest-cov/
[`.scpt`]: https://fileinfo.com/extension/scpt
[shell configuration file]: https://en.wikipedia.org/wiki/Unix_shell#Configuration_files
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
