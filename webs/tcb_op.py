from base.base import BasePage
from utils.utils import Util

class TcbOp(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    _link_to_chapters = "block.border.border-border.bg-card.mb-3.p-3.rounded" # class
    _title_list = "text-lg.font-bold" # class
    _chapter_images = "fixed-ratio" # class

    def get_chapter_images(self, chapter):
        chapters_checked = 3
        # Open the list of chapters
        self.wait_for_element(self._link_to_chapters, locator_type="class", condition="visible")
        list_of_chapters = self.get_elementList(self._link_to_chapters, locator_type="class")
        for container in list_of_chapters[:chapters_checked]:
            title = self.get_element(self._title_list, locator_type="class", parent=container)
            title_text = self.get_text(element=title)
            chapter_found = Util.verify_text_contains(self, chapter, title_text)
            if chapter_found:
                return True
            else:
                continue
        return False
