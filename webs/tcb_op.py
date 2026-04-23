from base.base import BasePage
from utils.utils import Util

class TcbOp(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    _link_to_chapters_class = "block.border.border-border.bg-card.mb-3.p-3.rounded"
    _title_list_class = "text-lg.font-bold"

    def get_chapter_images(self, chapter):
        chapters_checked = 3
        # Open the list of chapters
        self.wait_for_element(self._link_to_chapters_class, locator_type="class", condition="visible")
        list_of_chapters = self.get_elementList(self._link_to_chapters_class, locator_type="class")
        for container in list_of_chapters[:chapters_checked]:
            title = self.get_element(self._title_list_class, locator_type="class", parent=container)
            title_text = self.get_text(element=title)
            if Util.verify_text_contains(chapter, title_text):
                return True

        return False
