# Twin Galaxies Record Scraper

This project provides a Python-based web scraper to extract high-score records from the Twin Galaxies website, allowing users to gather and analyze game records efficiently.

![Interface](/github-images/interface.jpg)

## Features
* Game Record Scraping: Automatically collects every performance from a game page
* Filtering: Allows filtering by specific platforms or categories depending on the provided link
* Data Export: Outputs the collected data to a .xlsx file with induvidual category sheets (when applicable)

## Requirements
* [Google Chrome](https://www.google.com.br/chrome/index.html)
* Python >= 3.9, < 3.14
* Python's [tkinter package](https://docs.python.org/3/library/tkinter.html#module-tkinter)

Verify your current Python version and if tkinter is installed via Command Prompt / terminal:
```
python3 --version
python3 -m tkinter
```

If you're yet to install Python, download the installer from [python.org](https://www.python.org/downloads/). \
Alternatively, you may install it from the Microsoft Store and skip the next steps.

Make sure to select "Add python to PATH" on the very first screen of the installer. \
If you opt for a custom installation, select the optional feature "tcl/tk and IDLE" to include the tkinter package.

## Usage
You have the option to download and run one of the executables found in the [releases page](https://github.com/BrenoLudgero/Twin_Galaxies_Record_Scraper/releases).

In case the executable is not compatible with your system, follow the steps below.

## Preparing the enviroment
Download the source code from the [latest release](https://github.com/BrenoLudgero/Twin_Galaxies_Record_Scraper/releases).

Ensure that Python's package installer (pip) is installed and updated via Command Prompt / terminal:
```
python3 -m ensurepip
pip install --upgrade pip
```

Navigate to the source code folder via Command Prompt / terminal and install the required packages for this project:
```
cd PATH_TO_FOLDER/Twin_Galaxies_Record_Scraper
pip install -r requirements.txt
```

## Running from source
Execute `main.py`

## Creating an executable
Execute `builder.py`\
Your executable will be created in a new folder inside `dist/` by the end of the process.\
The new folder can be moved to another location, but its contents cannot.

## License
This project is licensed under the GNU General Public License. See the LICENSE file for more details.
