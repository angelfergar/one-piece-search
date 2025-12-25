from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

class WebDriverFactory():
    def get_webdriver(self, base_url):
        options = Options()
        options.headless = True
        options.add_argument("--headless")

        service = Service(GeckoDriverManager().install())

        driver = webdriver.Firefox(
            service=service,
            options=options
        )

        driver.set_window_size(1920, 1080)
        driver.get(base_url)
        return driver