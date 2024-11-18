import pandas as pd
from pathlib import Path
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException

driver = Driver(uc=True, headless=True)

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
        scroll_origin = ScrollOrigin.from_element(category_section)
        ActionChains(driver).scroll_from_origin(scroll_origin, 0, 200).perform()
        total_records = category_section.find_element(By.CSS_SELECTOR, "div.records").get_attribute("data-pcount")
        if total_records == "0":
            continue
        original_category_name = category_section.find_element(By.CSS_SELECTOR, "div.player-coun > b").text
        formatted_category_name = original_category_name.translate(str.maketrans("[]/:", "()|>"))[:31]
        records[formatted_category_name] = pd.DataFrame({})
        if int(total_records) > 5:
            show_performances_button = category_section.find_element(By.CSS_SELECTOR, "div.gd-other-links > a:nth-of-type(2)")
            show_performances_button.click()
            driver.switch_to.window(driver.window_handles[1])
            records_section = driver.find_element(By.CLASS_NAME, "gd-rank-list")
        else:
            records_section = category_section.find_element(By.CLASS_NAME, "gd-rank-list")
        category_records = records_section.find_elements(By.CSS_SELECTOR, "li > div:nth-child(1)")
        for record in category_records:
            player_name = record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > h5:nth-child(1) > a:nth-child(1)").text
            date_submitted = record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text
            esi = record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)").text
            score_type, points = record.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text.split("\n")
            record_row = {
                "Player": player_name,
                score_type: points,
                "ESI": esi,
                "Date Submitted": date_submitted,
            }
            records[formatted_category_name] = pd.concat(
                [records[formatted_category_name], pd.DataFrame([record_row])], ignore_index=True
            )
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
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
