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
        Instance._instance.quit()

    @staticmethod
    def close():
        if Instance._instance is None:
            return

        page_size = len(Instance._instance.window_handles)
        if page_size <= 1:
            return

        while page_size > 1:
            Instance._instance.switch_to.window(Instance._instance.window_handles[0])
            Instance._instance.close()
            page_size -= 1

        Instance._instance.switch_to.window(Instance._instance.window_handles[0])

    def __init__(self):
        if Instance._instance is not None:
            raise ValueError("only one instance can exist")

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        Instance._instance = webdriver.Chrome(options=chrome_options)
