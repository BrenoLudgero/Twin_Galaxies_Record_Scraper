import logging
from pandas import DataFrame
from selenium.webdriver.common.by import By
from .driver import *
from .navigator import *
from .error_detector import *
from utils.formatter import *
from config.setup import RECORDS_FOLDER_NAME
from utils.file_handler import export_data_to_excel

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

    def scrape_game_records(self, driver):
        records = {}
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
        return records

    def scrape_all_games(self, urls_to_scrape):
        if urls_to_scrape:
            logging.info("Scraping process initiated. Please wait.")
            for url in urls_to_scrape:
                try:
                    driver = create_driver()
                    game_page = ensure_proper_url(url, self.main_url)
                    driver.get(game_page)
                    if is_website_offline(driver):
                        logging.error("www.twingalaxies.com is currently offline")
                        break
                    elif is_invalid_page(driver, game_page):
                        logging.error(f"Invalid game page: {game_page}")
                        continue
                    logging.info(f"Scraping {game_page}")
                    records = self.scrape_game_records(driver)
                    if records:
                        file_name = get_formatted_file_name_from_url(game_page)
                        export_data_to_excel(records, file_name)
                        logging.info(f"Records saved to {RECORDS_FOLDER_NAME}/{file_name}.xlsx")
                    else:
                        logging.warning(f"No records for {game_page}")
                except Exception:
                    logging.critical("Uncaught exception:", exc_info=True)
                finally:
                    driver.quit()
            logging.info("Scraping process complete!")
        else:
            logging.error("List of games is empty.")
