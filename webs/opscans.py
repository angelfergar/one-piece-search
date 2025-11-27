from base.base import BasePage
from utils.utils import Util


class OpScans(BasePage):

    utils = Util()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _chapter_images = "ts-main-image.lazy" #class
    _consent_button = "//button[@aria-label='Consentir']"

    def get_chapter_images(self, chapter=None):
        self.wait_for_element(self._consent_button)
        self.element_click(self._consent_button)
        self.wait_for_element(self._chapter_images, locator_type="class", condition="visible")
        current_list = self.get_elementList(self._chapter_images, locator_type="class")
        if len(current_list) > 10:
            return True
        else:
            return False