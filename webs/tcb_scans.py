from base.base import BasePage
from utils.utils import Util

class TcbScans(BasePage):

    utils = Util()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _chapter_images = "//img[@decoding='async']"
    _consent_button = "//button[@aria-label='Consentir']"

    def get_chapter_images(self):
        self.wait_for_element(self._chapter_images, condition="visible")
        current_list = self.get_elementList(self._chapter_images)
        if len(current_list) > 1:
            return True
        else:
            return False