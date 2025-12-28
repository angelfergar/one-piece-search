from base.base import BasePage
from utils.utils import Util
from web_config import WebConfig
from datetime import datetime

class MangaPlus(BasePage):

    utils = Util()
    wc = WebConfig()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _text = "//span[contains(text(), 'próximo capítulo')]"

    def find_break_week(self):
        self.wait_for_element(locator=self._text, condition="visible")
        release_date = self.get_element(locator=self._text)
        release_text = self.get_text(element=release_date)
        date_release = release_text.split("el")[1].strip()
        release_format = datetime.strptime(date_release, "%A, %b %d, %H:%M")
        year, week, _ = release_format.isocalendar()
        return f'W{week}'


