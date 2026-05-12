Adapted from the [Python Docs](https://docs.python.org/3/tutorial/venv.html).
## Introduction
Python applications will often use packages and modules that don’t come as part of the standard library. Applications will sometimes need a specific version of a library, because the application may require that a particular bug has been fixed or the application may be written using an obsolete version of the library’s interface.

The solution for this problem is to create a [virtual environment](https://docs.python.org/3/glossary.html#term-virtual-environment), a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages.

If you're using Visual Studio Code it typically makes this process easier. Follow the below instructions if you're not using Visual Studio Code, or install Visual Studio Code using the other guides in this directory.
## Creating Virtual Environments
The module used to create and manage virtual environments is called [`venv`](https://docs.python.org/3/library/venv.html#module-venv "venv: Creation of virtual environments."). `venv` will install the Python version from which the command was run (as reported by the [`--version`](https://docs.python.org/3/using/cmdline.html#cmdoption-version) option). For instance, executing the command with `python3.12` will install version 3.12.

To create a virtual environment, decide upon a directory where you want to place it, and run the [`venv`](https://docs.python.org/3/library/venv.html#module-venv "venv: Creation of virtual environments.") module as a script with the directory path:
```sh
python -m venv .venv
```
**On Windows, you run the above command in PowerShell. On Mac, you run it in Terminal.** The above command will create the `.venv` directory if it doesn't exist, and also create directories inside it containing a copy of the Python interpreter and various supporting files.
You can choose any name for the `venv`, but `.venv` is often chosen because the `.` at the beginning keeps the directory hidden and thus out of the way while giving it a name that explains why the directory exists.

### Activating the virtual environment
**On Windows (Powershell):**
```sh
.venv\Scripts\activate
```
**On Mac/Linux (Terminal):**
```sh
source .venv/bin/activate
```
## Installing and managing packages with `pip`
You can install, upgrade, and remove packages using a program called **pip**. By default `pip` will install packages from the [Python Package Index](https://pypi.org). You can browse the Python Package Index by going to it in your web browser.

Generally you can install the latest version of a package by specifying a package's name:
```sh
python -m pip install pandas
```

For this repo I've put all of the requirements in one `requirements.txt` file. First make sure you are inside the main folder (root directory) of the cloned repository with the following command:
```sh
pwd
```
It should return some output that ends in `CERCET` (the name of the repository). If not, open a new PowerShell or Terminal window in the folder that was created when you ran the `git clone` command.

Run the following command to tell `pip` to install all of the packages in that file. 
```sh
python -m pip install -r requirements.txt
```

If this runs successfully you should have the necessary packages to run the Python scripts in this repository. 
If you get some error saying things like "this environment is externally managed" you may need to either:
	(1) move the python scripts into the main folder of the repository so they use the `venv` you created, or
	(2) make a new `venv` in the scripts directory inside the repository.
