import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions


def html_to_image(html_filename: str, save_as: str):
    """Salva o HTML informado no formato imagem PNG

    Args:
        html_filename (str): Nome do arquivo HTML
        save_as (str): Nome da imagem que será gerada (Sem extensão)
    """
    options = ChromiumOptions()
    # desabilita ambiente sandbox
    options.add_argument("--no-sandbox")
    # executa o navegador sem interface gráfica
    options.add_argument("--headless")
    # maximiza o navegador, para ocupar toda a tela
    options.add_argument("--start-maximized")
    # desabilita a aceleração de hardware por GPU
    options.add_argument("--disable-gpu")

    driver = webdriver.ChromiumEdge(options=options)

    html_file = Path.cwd() / f"tmp/{html_filename}"

    driver.get(html_file.as_uri())

    height = driver.execute_script("return document.documentElement.scrollHeight")
    width = driver.execute_script("return document.documentElement.scrollWidth")
    driver.set_window_size(width, height)

    time.sleep(1)

    driver.save_screenshot(f"tmp/{save_as}.png")
    driver.quit()
