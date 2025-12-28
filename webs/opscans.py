from base.base import BasePage


class OpScans(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    _chapter_images = "ts-main-image.lazy" #class
    _consent_button = "//button[@aria-label='Consentir']"

    def get_chapter_images(self, chapter=None):
        min_images_required = 10
        self.wait_for_element(self._consent_button)
        self.element_click(self._consent_button)
        self.wait_for_element(self._chapter_images, locator_type="class", condition="visible")
        current_list = self.get_elementList(self._chapter_images, locator_type="class")
        if len(current_list) > min_images_required:
            return True
        else:
            return False