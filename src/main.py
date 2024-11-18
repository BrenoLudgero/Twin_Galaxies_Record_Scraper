from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,1000")

driver = webdriver.Chrome(options=options)
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
