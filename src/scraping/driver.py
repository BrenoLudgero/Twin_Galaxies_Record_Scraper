from seleniumbase import Driver

def create_driver():
    driver = Driver(uc=True, headless=True, pls="eager", block_images=True)
    driver.maximize_window()
    return driver
