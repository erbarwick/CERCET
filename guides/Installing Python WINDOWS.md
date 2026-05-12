## Installation method 1: Microsoft Store or python.org
Adapted from the [Python Docs](https://docs.python.org/3/using/windows.html). If you run into trouble, that guide might provide some more guidance.

The Python install manager can be installed from the [Microsoft Store app](https://apps.microsoft.com/detail/9NQ7512CXL7T) or downloaded and installed from [python.org/downloads](https://www.python.org/downloads/). The two versions are identical.

**To install through the Store**, simply click "Install". After it has completed, open a terminal (on Windows it is called 'PowerShell') and type `python` to get started.
**To install the file downloaded from python.org,** double-click it and select "Install".
### After installation:
The `python`, `py`, and `pymanager` commands should be available in PowerShell. The recommended command for launching Python is `python`.
## Installation method 2: Windows PowerShell and `WinGet`
From [Microsoft's guide](https://learn.microsoft.com/en-us/windows/dev-environment/python?tabs=winget):

1. Open PowerShell in Windows Terminal and install Python with the following command:
```
winget install Python.Python.3.14
```
2. Use PowerShell to Install Visual Studio Code for easier script editing and running: 
```
winget install Microsoft.VisualStudioCode
```
3. Close and reopen PowerShell, then verify Python is installed:
```
python --version
```
4. Open VS Code and install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) from the VS Code Marketplace.

Done!

## Basic use
The recommended command for launching Python is `python`, which will either launch the version requested by the script being launched, an active virtual environment, or the default installed version, which will be the latest stable release unless configured otherwise. If no version is specifically requested and no runtimes are installed at all, the current latest release will be installed automatically.

For all scenarios involving multiple runtime versions, the recommended command is `py`. This may be used anywhere in place of `python` or the older `py.exe` launcher. By default, `py` matches the behaviour of `python`, but also allows command line options to select a specific version as well as subcommands to manage installations. These are detailed below.

Because the `py` command may already be taken by the previous version, there is also an unambiguous `pymanager` command. Scripted installs that are intending to use Python install manager should consider using `pymanager`, due to the lower chance of encountering a conflict with existing installs. The only difference between the two commands is when running without any arguments: `py` will launch your default interpreter, while `pymanager` will display help (`pymanager exec ...` provides equivalent behaviour to `py ...`).

Each of these commands also has a windowed version that avoids creating a console window. These are `pyw`, `pythonw` and `pymanagerw`. A `python3` command is also included that mimics the `python` command. It is intended to catch accidental uses of the typical POSIX command on Windows, but is not meant to be widely used or recommended.

To launch your default runtime, run `python` or `py` with the arguments you want to be passed to the runtime (such as script files or the module to launch):

$> py
...
$> python my-script.py
...
$> py -m this
...

The default runtime can be overridden with the [`PYTHON_MANAGER_DEFAULT`](https://docs.python.org/3/using/windows.html#envvar-PYTHON_MANAGER_DEFAULT) environment variable, or a configuration file. See [Configuration](https://docs.python.org/3/using/windows.html#pymanager-config) for information about configuration settings.

To launch a specific runtime, the `py` command accepts a `-V:<TAG>` option. This option must be specified before any others. The tag is part or all of the identifier for the runtime; for those from the CPython team, it looks like the version, potentially with the platform. For compatibility, the `V:` may be omitted in cases where the tag refers to an official release and starts with `3`.

$> py -V:3.14 ...
$> py -V:3-arm64 ...

Runtimes from other distributors may require the _company_ to be included as well. This should be separated from the tag by a slash, and may be a prefix. Specifying the company is optional when it is `PythonCore`, and specifying the tag is optional (but not the slash) when you want the latest release from a specific company.

$> py -V:Distributor\1.0 ...
$> py -V:distrib/ ...

If no version is specified, but a script file is passed, the script will be inspected for a _shebang line_. This is a special format for the first line in a file that allows overriding the command. See [Shebang lines](https://docs.python.org/3/using/windows.html#pymanager-shebang) for more information. When there is no shebang line, or it cannot be resolved, the script will be launched with the default runtime.

If you are running in an active virtual environment, have not requested a particular version, and there is no shebang line, the default runtime will be that virtual environment. In this scenario, the `python` command was likely already overridden and none of these checks occurred. However, this behaviour ensures that the `py` command can be used interchangeably.

When no runtimes are installed, any launch command will try to install the requested version and launch it. However, after any version is installed, only the `py exec ...` and `pymanager exec ...` commands will install if the requested version is absent. Other forms of commands will display an error and direct you to use `py install` first.