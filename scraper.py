import logging
import traceback
from pandas import DataFrame
from selenium.webdriver.common.by import By
from utils import *
from navigation import *
from driver import create_driver
from error_handler import page_errors_detected
from config import FOLDER_NAME

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
            score_type, points = record.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text.split("\n")
            record_data = {
                "Player": record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > h5:nth-child(1) > a:nth-child(1)").text,
                "Date Submitted": record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text,
                "ESI": record.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > span:nth-child(2)").text,
                score_type: points,
            }
            category_records.append(record_data)
        close_performances_tab_if_open(driver)
        return DataFrame(category_records)

    def scrape_game_records(self, url):
        driver = create_driver()
        records = {}
        try:
            driver.get(url)
            if page_errors_detected(driver, url):
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

    def scrape_all_games(self, urls_to_scrape):
        if urls_to_scrape:
            logging.info("Scraping process initiated. Please wait.")
            for url in urls_to_scrape:
                try:
                    game_page = ensure_proper_url(url, self.main_url)
                    logging.info(f"Scraping {game_page}")
                    records = self.scrape_game_records(game_page)
                    if records:
                        file_name = get_formatted_file_name_from_url(game_page)
                        save_to_excel(records, file_name)
                        logging.info(f"Records saved to {FOLDER_NAME}/{file_name}.xlsx")
                except Exception:
                    logging.critical("Uncaught exception:", exc_info=True)
            logging.info("Scraping process complete!")
        else:
            logging.error("List of games is empty.")
