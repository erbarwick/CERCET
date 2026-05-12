Adapted from the [Python Docs](https://docs.python.org/3/using/mac.html)
## Installation
1. Download the "macOS installer" for the latest Stable Release from the [Python Releases for macOS page.](https://www.python.org/downloads/macos/)
2. For a default installation, double-click on the downloaded installer package file. This should launch the standard macOS Installer app and display the first of several installer windows steps.
3. Go through the **Install Python** window until it says "The installation was completed successfully." Then you can Close the installer window.
4. Double-click on the **Install Certificates.command** icon or file in the `/Applications/Python 3.14/` window to complete the installation.
	- This will open a temporary **Terminal** shell window that will use the new Python to download and install SSL root certificates for its use.
	- If `Successfully installed certifi` and `update complete` appears in the terminal window, the installation is complete. Close this terminal window and the installer window.

## How to run a Python script
**Note: The scripts in this repository will not work until you install the required packages. See the [[Creating Python virtual environments and installing packages]] guide in this folder for more information.**

There are two ways to invoke the Python interpreter. If you are familiar with using a Unix shell in a terminal window, you can invoke `python3.14` or `python3` optionally followed by one or more command line options (described in [Command line and environment](https://docs.python.org/3/using/cmdline.html#using-on-general)). The Python tutorial also has a useful section on [using Python interactively from a shell](https://docs.python.org/3/tutorial/appendix.html#tut-interac).

You can also invoke the interpreter through an integrated development environment. [IDLE — Python editor and shell](https://docs.python.org/3/library/idle.html#idle) is a basic editor and interpreter environment which is included with the standard distribution of Python. **IDLE** includes a Help menu that allows you to access Python documentation. If you are completely new to Python, you can read the tutorial introduction in that document.

There are many other editors and IDEs available, see [Editors and IDEs](https://docs.python.org/3/using/editors.html#editors) for more information.

To run a Python script file from the terminal window, you can invoke the interpreter with the name of the script file:

> `python3.14` `myscript.py`

To run your script from the Finder, you can either:

- Drag it to **Python Launcher**.
    
- Select **Python Launcher** as the default application to open your script (or any `.py` script) through the Finder Info window and double-click it. **Python Launcher** has various preferences to control how your script is launched. Option-dragging allows you to change these for one invocation, or use its `Preferences` menu to change things globally.
    

Be aware that running the script directly from the macOS Finder might produce different results than when running from a terminal window as the script will not be run in the usual shell environment including any setting of environment variables in shell profiles. And, as with any other script or program, be certain of what you are about to run.