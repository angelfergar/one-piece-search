from base.base import BasePage
from utils.utils import Util

class TcbScans(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        util = Util()

    # Locators
    _link_to_chapters_class = "post-details"
    _title_list_class = "post-title"
    _updated = "(//div[@class='post-meta clearfix'])/span"

    minutes_text = "minutes ago"

    def get_chapter_images(self, chapter):
        # Open the list of chapters
        self.wait_for_element(self._link_to_chapters_class, locator_type="class", condition="visible")
        list_of_chapters = self.get_elementList(self._link_to_chapters_class, locator_type="class")

        for container in list_of_chapters:
            title = self.get_element(self._title_list_class, locator_type="class", parent=container)
            title_text = self.get_text(element=title)

            if Util.verify_text_contains(chapter, title_text):
                updated = self.get_element(self._updated, parent=container)
                updated_text = self.get_text(element=updated)
                if Util.verify_text_contains(self.minutes_text, updated_text):
                    return True

        return False
