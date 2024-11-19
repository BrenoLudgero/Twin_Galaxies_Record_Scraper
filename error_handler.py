from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def is_invalid_page(driver, game_page):
    try:
        driver.find_element(By.CSS_SELECTOR, ".panel-body > div:nth-child(1) > div:nth-child(1)")
        print(f"[ERROR] Invalid game page: {game_page}")
        return True
    except NoSuchElementException:
        return False

def is_website_offline(driver):
    try:
        driver.find_element(By.ID, "cf-error-details")
        print("[ERROR] TwinGalaxies is currently offline")
        return True
    except NoSuchElementException:
        return False

def page_errors_detected(driver, game_page):
    if is_invalid_page(driver, game_page) or is_website_offline(driver):
        return True
    return False
