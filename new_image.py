import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

html_file = Path.cwd() / "new_image.html"

driver.get(html_file.as_uri())

time.sleep(2)

height = driver.execute_script("return document.documentElement.scrollHeight")
width = driver.execute_script("return document.documentElement.scrollWidth")
driver.set_window_size(width, height)

time.sleep(2)
driver.save_screenshot("screenshot2.png")
driver.quit()
