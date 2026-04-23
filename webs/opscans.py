from base.base import BasePage

class OpScans(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    _chapter_images_class = "ts-main-image.lazy"
    _consent_button = "//button[@aria-label='Consentir']"

    def get_chapter_images(self, chapter=None):
        min_images_required = 10
        try:
            self.wait_for_element(self._consent_button)
            self.element_click(self._consent_button)
        except Exception:
            pass # Consent window didn't appear
        self.wait_for_element(self._chapter_images_class, locator_type="class", condition="visible")
        current_list = self.get_elementList(self._chapter_images_class, locator_type="class")
        return len(current_list) > min_images_required
