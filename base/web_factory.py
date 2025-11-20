from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class WebDriverFactory():

    def get_webdriver(self, base_url):
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)

        driver.get(base_url)
        return driver
