import PyInstaller.__main__
from utils.file_handler import get_root_directory

PyInstaller.__main__.run([
    f"{get_root_directory()}/src/main.py",
    "--clean",
    "--onedir",
    "--noconsole",
    "-nTG Record Scraper",
])
