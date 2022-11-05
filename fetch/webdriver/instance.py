from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions

from .settings import Settings


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
        options = FirefoxOptions()
        options.headless = True
        service = Service(Settings.Path.value)
        driver = webdriver.Firefox(service=service, options=options)
        Instance._instance = driver
