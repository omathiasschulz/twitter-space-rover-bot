import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def html_to_image(html_content: str, save_as: str):
    """Salva o HTML informado no formato imagem PNG

    Args:
        html_content (str): HTML para converter como imagem
        save_as (str): Nome da imagem que será gerada
    """
    chrome_options = Options()
    # executa o navegador sem interface gráfica
    chrome_options.add_argument("--headless")
    # maximiza o navegador, para ocupar toda a tela
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.ChromiumEdge(options=chrome_options)

    # html_file = Path.cwd() / f"{html_content}.html"
    # driver.get(html_file.as_uri())
    driver.get(f"data:text/html;charset=utf-8,{html_content}")

    height = driver.execute_script("return document.documentElement.scrollHeight")
    width = driver.execute_script("return document.documentElement.scrollWidth")
    driver.set_window_size(width, height)

    time.sleep(1)

    driver.save_screenshot(f"{save_as}.png")
    driver.quit()
