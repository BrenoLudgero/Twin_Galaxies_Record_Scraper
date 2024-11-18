import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,1000")

driver = webdriver.Chrome(options=options)
stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

main_url = "https://www.twingalaxies.com/game/"
game_path = "galaga/arcade/"
game_url = f"{main_url}{game_path}"
driver.get(game_url)

try:
    error_message_element = driver.find_element(By.CSS_SELECTOR, ".panel-body > div:nth-child(1) > div:nth-child(1)")
    print(f"[ERROR] Invalid game page: {main_url}")
    driver.quit()
    quit()
except NoSuchElementException:
    pass

records = {}

while True:
    category_sections = driver.find_elements(By.CLASS_NAME, "game-post")
    for category_section in category_sections:
        total_records = category_section.find_element(By.CSS_SELECTOR, "div.records").get_attribute("data-pcount")
        if total_records == "0":
            continue
        original_category_name = category_section.find_element(By.CSS_SELECTOR, "div.player-coun > b").text
        formatted_category_name = original_category_name.translate(str.maketrans("[]/", "()|"))[:31]
        records[formatted_category_name] = pd.DataFrame({
            "Player": [],
            "Points": [],
            "ESI": [],
            "Date Submitted": [],
        })
        records_section = category_section.find_element(By.CLASS_NAME, "gd-rank-list")
        category_records = records_section.find_elements(By.CSS_SELECTOR, "li > div:nth-child(1)")
        for record in category_records:
            player_name = record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > h5:nth-child(1) > a:nth-child(1)").text
            date_submitted = record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text
            esi = record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)").text
            try:
                points = record.find_element(By.CSS_SELECTOR, "div:nth-child(4) > h3:nth-child(2) > a:nth-child(1)").text
            except NoSuchElementException:
                points = record.find_element(By.CSS_SELECTOR, "div:nth-child(4) > h3:nth-child(2)").text
            record_row = {
                "Player": player_name,
                "Points": points,
                "ESI": esi,
                "Date Submitted": date_submitted,
            }
            records[formatted_category_name] = pd.concat(
                [records[formatted_category_name], pd.DataFrame([record_row])], ignore_index=True
            )
    page_navigation_section = driver.find_element(By.ID, "paginn")
    ActionChains(driver).move_to_element(page_navigation_section).perform()
    page_navigation_buttons = page_navigation_section.find_elements(By.CLASS_NAME, "pagesPagination")
    last_navigation_button = page_navigation_buttons[-1]
    if last_navigation_button.text == "Next":
        last_navigation_button.click()
    else:
        driver.quit()
        break

current_directory = Path(__file__).parent
Path(f"{current_directory}/TG_Records/").mkdir(exist_ok=True)

file_name = game_path[:-1] if game_path.endswith("/") else game_path
file_name = file_name.replace("/", "_").lower()

with pd.ExcelWriter(f"TG_Records/{file_name}.xlsx", engine="openpyxl") as writer:
    for category, data in records.items():
        data.to_excel(writer, sheet_name=category, index=False)
