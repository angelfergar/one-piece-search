from base.web_factory import WebDriverFactory

class WebConfig():

    def set_up(self,base_url):
        wdf = WebDriverFactory()
        driver = wdf.get_webdriver(base_url=base_url)
        return driver
