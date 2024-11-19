from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

def open_performances_in_new_tab(driver, category_section):
    button = category_section.find_element(By.CSS_SELECTOR, "div.gd-other-links > a:nth-of-type(2)")
    ActionChains(driver).scroll_to_element(button).perform()
    button.click()
    driver.switch_to.window(driver.window_handles[1])

def close_performances_tab_if_open(driver):
    if len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def go_to_next_page_if_available(driver):
    try:
        page_navigation = driver.find_element(By.ID, "paginn")
        ActionChains(driver).move_to_element(page_navigation).perform()
        next_button = page_navigation.find_elements(By.CLASS_NAME, "pagesPagination")[-1]
        if next_button.text == "Next":
            next_button.click()
            return True
    except (NoSuchElementException, IndexError):
        return False
