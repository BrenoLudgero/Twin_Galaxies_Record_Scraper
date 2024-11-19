from seleniumbase import Driver

def create_driver():
    driver = Driver(uc=True, headless2=True, block_images=True)
    driver.maximize_window()
    return driver
