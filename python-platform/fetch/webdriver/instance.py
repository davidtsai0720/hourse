# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium.webdriver import ChromiumDriver


class Instance:

    _instance = None

    @staticmethod
    def get_instance() -> ChromiumDriver:
        if Instance._instance is None:
            Instance()
        return Instance._instance

    @staticmethod
    def reset():
        if Instance._instance is None:
            return
        Instance._instance.close()
        Instance._instance.quit()

    def __init__(self):
        if Instance._instance is not None:
            raise Exception('only one instance can exist')

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--window-size=1920,1080')
        Instance._instance = webdriver.Chrome(options=chrome_options)
        assert isinstance(Instance._instance, ChromiumDriver), 'Should be ChromiumDriver'
