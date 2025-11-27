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
    _chapter_title = "//h1[contains(text(), 'One Piece')]"

    def get_chapter_images(self, chapter):
        self.wait_for_element(self._chapter_images, condition="visible")
        self.wait_for_element(self._chapter_title, condition="visible")
        current_list = self.get_elementList(self._chapter_images)
        chapter_num = self.get_text(self._chapter_title)
        if len(current_list) > 10 and self.utils.verify_text_contains(chapter, chapter_num):
            return True
        else:
            return False