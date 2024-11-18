import pandas as pd
from pathlib import Path
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException

main_url = "https://www.twingalaxies.com/game/"

records = {}

paths_to_scrape = [
    "galaga/arcade",
    "devils-crush/turbografx-16",
    "burnout-2-point-of-impact/nintendo-game-cube/",
]

for game_path in paths_to_scrape:
    driver = Driver(uc=True, headless=True)
    game_page = f"{main_url}{game_path}"
    driver.get(game_page)
    try:
        driver.find_element(By.CSS_SELECTOR, ".panel-body > div:nth-child(1) > div:nth-child(1)")
        print(f"[ERROR] Invalid game page: {main_url}")
        driver.quit()
        quit()
    except NoSuchElementException:
        pass
    try:
        driver.find_element(By.ID, "cf-error-details")
        print(f"[ERROR] TwinGalaxies is currently offline")
        driver.quit()
        quit()
    except NoSuchElementException:
        pass
    records[game_path] = {}
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
            records[game_path][formatted_category_name] = pd.DataFrame({})
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
                records[game_path][formatted_category_name] = pd.concat(
                    [records[game_path][formatted_category_name], pd.DataFrame([record_row])], ignore_index=True
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

for game, categories in records.items():
    file_name = game[:-1] if game.endswith("/") else game
    file_name = file_name.replace("/", "_").lower()
    with pd.ExcelWriter(f"TG_Records/{file_name}.xlsx", engine="openpyxl") as writer:
        for category_name, category_data in categories.items():
            category_data.to_excel(writer, sheet_name=category_name, index=False)
