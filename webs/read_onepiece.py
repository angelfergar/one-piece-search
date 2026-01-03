from base.base import BasePage
from utils.utils import Util


class ReadOnePiece(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    _chapter_list = "chapter-list" # ID
    _chapters = "chapter-item" # class
    _title_chapter = "chapter-number" # class

    def get_chapter_images(self, chapter):
        chapters_checked = 3
        self.wait_for_element(self._chapter_list, locator_type="id", condition="visible")
        current_list = self.get_elementList(self._chapters, locator_type="class")
        for container in current_list[:chapters_checked]:
            title = self.get_element(self._title_chapter, locator_type="class", parent=container)
            title_text = self.get_text(element=title)
            chapter_found = Util.verify_text_contains(self, actual_text=chapter, expected_text=title_text)
            if chapter_found:
                return True
            else:
                continue
        return False
