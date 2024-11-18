import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,1000")

driver = webdriver.Chrome(options=options)
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

main_url = "https://www.twingalaxies.com/game/"
game_path = "galaga/arcade/"
game_page = f"{main_url}{game_path}"

records = {
    "Category": pd.DataFrame({
        "Date Submitted": [],
        "ESI": [],
        "Points": [],
    })
}

current_directory = Path(__file__).parent
Path(f"{current_directory}/TG_Records/").mkdir(exist_ok=True)

file_name = game_path[:-1] if game_path.endswith("/") else game_path
file_name = file_name.replace("/", "_")

with pd.ExcelWriter(f"TG_Records/{file_name}.xlsx", engine="openpyxl") as writer:
    for category, data in records.items():
        data.to_excel(writer, sheet_name=category, index=False)
