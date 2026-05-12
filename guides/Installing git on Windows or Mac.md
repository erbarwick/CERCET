Adapted from [Git Guides](https://github.com/git-guides/install-git)
## Checking for Git
To see if you already have Git installed, open up your terminal application.
- If you're on a Mac, look for a command prompt application called "Terminal".
- If you're on a Windows machine, open the windows command prompt or "Git Bash".
Once you've opened your terminal application, type `git version`. The output will either tell you which version of Git is installed, or it will alert you that `git` is an unknown command. If it's an unknown command, read further and find out how to install Git.

## Install Git on Windows
1. Navigate to the latest [Git for Windows installer](https://gitforwindows.org/) and download the latest version.
2. Once the installer has started, follow the instructions as provided in the **Git Setup** wizard screen until the installation is complete.
3. Open the windows command prompt (or **Git Bash** if you selected not to use the standard Git Windows Command Prompt during the Git installation).
4. Type `git version` to verify Git was installed.
Note: [`git-scm`](https://git-scm.com/download/win) is a popular and recommended resource for downloading Git for Windows. The advantage of downloading Git from `git-scm` is that your download automatically starts with the latest version of Git included with the recommended command prompt, `Git Bash` . The download source is the same [Git for Windows installer](https://gitforwindows.org/) as referenced in the steps above.
## Install Git on Windows through Visual Studio Code
GitHub integration is provided through the [GitHub Pull Requests and Issues extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github).  
To get started with the GitHub in VS Code, you'll need to create an account and install the GitHub Pull Requests and Issues extension.  
Once you've installed the [GitHub Pull Requests and Issues extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github), you'll need to sign in. Follow the prompts to authenticate with GitHub and return to VS Code.

---

Note: You can perform actions like, you can search for and clone a repository from GitHub using the Git: Clone command in the Command Palette (Ctrl+Shift+P) or by using the Clone Repository button in the Source Control view (available when you have no folder open).  
[Learn more here](https://code.visualstudio.com/docs/editor/github)

## Install Git on Mac
Most versions of MacOS will already have `Git` installed, and you can activate it through the terminal with `git version`. However, if you don't have Git installed for whatever reason, you can install the latest version of Git using one of several popular methods as listed below:

### Install Git From an Installer
1. Navigate to the latest [macOS Git Installer](https://sourceforge.net/projects/git-osx-installer/files/git-2.23.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect) and download the latest version.
2. Once the installer has started, follow the instructions as provided until the installation is complete.
3. Open the command prompt "terminal" and type `git version` to verify Git was installed.

Note: [`git-scm`](https://git-scm.com/download/mac) is a popular and recommended resource for downloading Git on a Mac. The advantage of downloading Git from `git-scm` is that your download automatically starts with the latest version of Git. The download source is the same [macOS Git Installer](https://sourceforge.net/projects/git-osx-installer/files/git-2.23.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect) as referenced in the steps above.

### Install Git from Homebrew
[Homebrew](https://brew.sh/) is a popular package manager for macOS. If you already have Homebrew installed, you can follow the below steps to install Git:

1. Open up a terminal window and install Git using the following command: `brew install git`.
2. Once the command output has been completed, you can verify the installation by typing: `git version`.