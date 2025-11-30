import base64

from base.base import BasePage
from utils.utils import Util
from rapidfuzz import fuzz

class TcbScans(BasePage):

    utils = Util()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _chapter_images = "//img[@decoding='async']"
    _first_image = "(//img[@decoding='async'])[1]"
    _consent_button = "//button[@aria-label='Consentir']"
    _chapter_title = "//h1[contains(text(), 'One Piece')]"

    def get_chapter_images(self, chapter):
        self.wait_for_element(self._chapter_images, condition="visible")
        self.wait_for_element(self._chapter_title, condition="visible")
        current_list = self.get_elementList(self._chapter_images)
        self.driver.execute_script("document.body.style.zoom = '500%'")
        self.scroll_toElement(locator=self._first_image)
        self.driver.save_screenshot('my_image.png')
        chapter_number = self.utils.get_image_number()
        match_score = fuzz.partial_ratio(chapter_number, chapter)
        if len(current_list) > 10 and match_score >= 75:
            return True
        else:
            return False