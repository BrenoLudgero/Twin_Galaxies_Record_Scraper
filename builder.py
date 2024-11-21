import PyInstaller.__main__

# Run this file to export the program to an executable
PyInstaller.__main__.run([
    "main.py",
    "--clean",
    "--onedir",
    "--noconsole",
    "-nTG Record Scraper",
])
