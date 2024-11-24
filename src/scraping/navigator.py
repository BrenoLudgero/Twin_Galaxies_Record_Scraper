from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

def open_performances_in_new_tab(driver, category_section):
    more_performances_button = category_section.find_element(By.CSS_SELECTOR, "div.gd-other-links > a:nth-of-type(2)")
    ActionChains(driver).scroll_to_element(more_performances_button).perform()
    more_performances_button.click()
    driver.switch_to.window(driver.window_handles[1])

def close_performances_tab_if_open(driver):
    if len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def go_to_next_page_if_available(driver):
    try:
        navigation_section = driver.find_element(By.ID, "paginn")
        ActionChains(driver).move_to_element(navigation_section).perform()
        last_button = navigation_section.find_elements(By.CLASS_NAME, "pagesPagination")[-1]
        if last_button.text == "Next":
            last_button.click()
            return True
    except (NoSuchElementException, IndexError):
        return False
