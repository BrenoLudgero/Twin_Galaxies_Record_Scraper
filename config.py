from pathlib import Path

MAIN_URL = "https://www.twingalaxies.com/game/"

CURRENT_DIRECTORY = Path(__file__).parent
RECORDS_FOLDER_DIRECTORY = CURRENT_DIRECTORY / "TG Records"
RECORDS_FOLDER_DIRECTORY.mkdir(exist_ok=True)

PATHS_TO_SCRAPE = [
    "_",
    "galaga/arcade",
    "devils-crush/turbografx-16/",
    "burnout-2-point-of-impact/nintendo-game-cube",
    "mame-5-minute-challenge-2023/mame/qix-5-minute",
]
