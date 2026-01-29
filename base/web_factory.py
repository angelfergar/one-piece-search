from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class WebDriverFactory():
    def get_webdriver(self, base_url):
        options = Options()
        options.add_argument("-headless")

        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
        driver.get(base_url)
        return driver