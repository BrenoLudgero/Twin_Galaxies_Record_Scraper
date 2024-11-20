from threading import Thread
from pandas import DataFrame
from selenium.webdriver.common.by import By
from utils import *
from navigation import *
from driver import create_driver
from error_handler import page_errors_detected
from config import FOLDER_NAME, RECORDS_FOLDER_DIRECTORY

class RecordScraper:
    def __init__(self):
        self.main_url = "https://www.twingalaxies.com/game/"

    def get_performances_section(self, driver, category_section):
        total_records = int(category_section.find_element(By.CSS_SELECTOR, "div.records").get_attribute("data-pcount"))
        if total_records > 5:
            open_performances_in_new_tab(driver, category_section)
            return driver.find_element(By.CLASS_NAME, "gd-rank-list")
        return category_section.find_element(By.CLASS_NAME, "gd-rank-list")

    def scrape_category_records(self, driver, category_section):
        category_records = []
        records_section = self.get_performances_section(driver, category_section)
        record_elements = records_section.find_elements(By.CSS_SELECTOR, "li > div:nth-child(1)")
        for record in record_elements:
            record_data = {
                "Player": record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > h5:nth-child(1) > a:nth-child(1)").text,
                "Date Submitted": record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text,
                "ESI": record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)").text,
                **dict(zip(["Score Type", "Points"], record.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text.split("\n"))),
            }
            category_records.append(record_data)
        close_performances_tab_if_open(driver)
        return DataFrame(category_records)

    def scrape_game_records(self, game_path):
        driver = create_driver()
        records = {}
        try:
            game_page = ensure_proper_page_link(game_path, self.main_url)
            driver.get(game_page)
            if page_errors_detected(driver, game_page):
                return {}
            while True:
                category_sections = driver.find_elements(By.CLASS_NAME, "game-post")
                for section in category_sections:
                    total_records = section.find_element(By.CSS_SELECTOR, "div.records").get_attribute("data-pcount")
                    if total_records == "0":
                        continue
                    category_name = sanitize_category_name(section.find_element(By.CSS_SELECTOR, "div.player-coun > b").text)
                    records[category_name] = self.scrape_category_records(driver, section)
                if not go_to_next_page_if_available(driver):
                    break
        finally:
            driver.quit()
        return records

    def scrape_all_games(self, paths_to_scrape):
        if paths_to_scrape:
            print(f"[INFO] Scraping process initiated. Please wait.")
            for game_path in paths_to_scrape:
                records = self.scrape_game_records(game_path)
                if records:
                    file_name = get_formatted_file_name_from_url(game_path)
                    save_to_excel(records, file_name, RECORDS_FOLDER_DIRECTORY)
                    print(f"[INFO] Records saved to {FOLDER_NAME}/{file_name}")
            print(f"[INFO] Scraping process complete!")
        else:
            print(f"[ERROR] List of games is empty.")

    def run(self, paths_to_scrape):
        Thread(target=self.scrape_all_games, args=(paths_to_scrape,)).start()
