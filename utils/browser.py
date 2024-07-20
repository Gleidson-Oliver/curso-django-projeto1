import os
import time  # Adicionar biblioteca para tempo de espera
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / \
    'chromedriver-linux64' / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    """ chrome_options.binary_location = CHROME_EXECUTABLE_PATH """
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    # Adicionar opções de log
    chrome_service = Service(
        executable_path=CHROMEDRIVER_PATH)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':

    browser = make_chrome_browser('--headless')
    browser.get('http://www.google.com/')
    time.sleep(5)
