from pandas import DataFrame
from selenium.webdriver.common.by import By
from navigation import *
from driver import create_driver
from utils import sanitize_category_name
from error_handler import page_errors_detected

class RecordScraper:
    def __init__(self, main_url):
        self.main_url = main_url

    def scrape_game_records(self, game_path):
        driver = create_driver()
        records = {}
        try:
            game_page = f"{self.main_url}{game_path}"
            driver.get(game_page)
            if page_errors_detected(driver, game_page):
                return {}
            while True:
                category_sections = driver.find_elements(By.CLASS_NAME, "game-post")
                for section in category_sections:
                    total_records = section.find_element(By.CSS_SELECTOR, "div.records").get_attribute("data-pcount")
                    if total_records == "0":
                        continue
                    category_name = sanitize_category_name(
                        section.find_element(By.CSS_SELECTOR, "div.player-coun > b").text
                    )
                    records[category_name] = self.scrape_category_records(driver, section)
                if not go_to_next_page_if_available(driver):
                    break
        finally:
            driver.quit()
        return records

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
                **dict(zip(
                    ["Score Type", "Points"],
                    record.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text.split("\n")
                )),
            }
            category_records.append(record_data)
        close_performances_tab_if_open(driver)
        return DataFrame(category_records)
