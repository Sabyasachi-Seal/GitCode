# GitCode & GitChef

These tools make it possible to extract all your solutions from [LeetCode](https://leetcode.com/) and
[CodeChef](https://codeshef.com) to your local machine and commit them to a git repository.

## Features

- Supports O-Auth login
- Supports user-pass login
- Creates folder for every of your problem solutions
- Exports all of your problem solutions in separate folders
- Additionally, exports problem descriptions with them
- Specify path for problem solutions
- Commit solution to git repository

## Usage

- [Setup Git](https://docs.github.com/en/get-started/quickstart/set-up-git) with your GitHub account on your local
  machine
- Optionally [fork](https://github.com/Sabyasachi-Seal/GitCode/fork) this repository
- Clone the repository on your local machine
- Install the projects' dependencies (see [Dependencies](#Dependencies))
- Run either `GitCode.py` or `GitChef.py` from the project root folder with:
    - `cd GitCode && python ./GitCode.py`
    - `cd GitChef && python ./GitChef.py`

### Dependencies

This project requires a working Python 3.6+ installation. If the `pip` package manager is installed and the system is
not externally managed (e.g. by the Linux distribution), the Python dependencies are installed automatically. If it is
externally managed, you need to install the packages listed in the `requirements.txt` file or use one of the commands
for your Linux distribution.

#### Arch Linux

This assumes that the AUR package install helper `paru` is installed. If another one is used, it can usually be
substituted with its name or the listed packages are cloned and built itself with `makepkg`.

```shell
# Install dependencies for GitCode
pacman -S python-pysocks python-async_generator python-attrs python-certifi \
          python-charset-normalizer python-exceptiongroup python-h11 python-idna \
          python-outcome python-packaging python-dotenv python-requests python-sniffio \
          python-sortedcontainers python-tqdm python-trio python-trio-websocket \
          python-urllib3 python-wsproto
paru -S python-selenium python-webdriver-manager python-pybrowsers python-poetry

# Install dependencies for GitChef
pacman -S python-html5lib python-lxml python-requests
paru -S python-bs4
```

## Contributors

Contributions and feedback are welcome!

- [Sabyasachi Seal](https://github.com/Sabyasachi-Seal)
- [AdityaSeth777](https://github.com/AdityaSeth777)
- [Ayush786113](https://github.com/Ayush786113)
