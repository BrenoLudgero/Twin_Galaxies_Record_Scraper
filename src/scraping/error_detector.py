from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def is_invalid_page(driver, game_page):
    try:
        driver.find_element(By.CSS_SELECTOR, ".panel-body > div:nth-child(1) > div:nth-child(1)")
        return True
    except NoSuchElementException:
        return False

def is_website_offline(driver):
    try:
        driver.find_element(By.ID, "cf-error-details")
        return True
    except NoSuchElementException:
        return False
