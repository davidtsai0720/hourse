from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Instance:

    _instance = None

    @staticmethod
    def get_instance():
        if Instance._instance is None:
            Instance()
        return Instance._instance

    @staticmethod
    def reset():
        if Instance._instance is None:
            Instance()
        Instance._instance.close()
        Instance._instance.quit()

    def __init__(self):
        if Instance._instance is not None:
            raise Exception('only one instance can exist')

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        Instance._instance = webdriver.Chrome(options=chrome_options)
