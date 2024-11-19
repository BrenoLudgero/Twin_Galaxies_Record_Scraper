import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--clean",
    "--onefile",
    "-nTG Record Scraper",
])
