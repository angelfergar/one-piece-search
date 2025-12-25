from base.base import BasePage
from utils.utils import Util

class TcbScans(BasePage):

    utils = Util()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _link_to_chapters = "post-details" # class
    _title_list = "post-title" # class
    _button_to_chapter = "more-link.button" # class
    _updated = "(//div[@class='post-meta clearfix'])/span"

    minutes_text = "minutes ago"


    def get_chapter_images(self, chapter):
        chapter_found = False
        true_updated = False
        # Open the list of chapters
        self.wait_for_element(self._link_to_chapters, locator_type="class", condition="visible")
        list_of_chapters = self.get_elementList(self._link_to_chapters, locator_type="class")

        for container in list_of_chapters:
            if not chapter_found:
                title = self.get_element(self._title_list, locator_type="class", parent=container)
                title_text = self.get_text(element=title)
                chapter_found = self.utils.verify_text_contains(chapter, title_text)
                if not true_updated:
                    updated = self.get_element(self._updated, parent=container)
                    updated_text = self.get_text(element=updated)
                    true_updated = self.utils.verify_text_contains(self.minutes_text, updated_text)
                    if true_updated:
                        return True
            else:
                continue
        return False