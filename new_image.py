import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# executa o navegador sem interface gráfica
chrome_options.add_argument("--headless")
# maximiza o navegador, para ocupar toda a tela
chrome_options.add_argument("--start-maximized")

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.ChromiumEdge(options=chrome_options)

html_content = "<html><head></head><body><h1>Conteúdo HTML</h1></body></html>"

driver.get(f"data:text/html;charset=utf-8,{html_content}")

height = driver.execute_script("return document.documentElement.scrollHeight")
width = driver.execute_script("return document.documentElement.scrollWidth")
driver.set_window_size(width, height)

time.sleep(1)

driver.save_screenshot("apod_5.png")
driver.quit()
