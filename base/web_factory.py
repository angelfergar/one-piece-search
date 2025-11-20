from selenium import webdriver

class WebDriverFactory():

    def get_webdriver(self, base_url):
        driver = webdriver.Firefox()

        driver.maximize_window()
        driver.get(base_url)

        return driver